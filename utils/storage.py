import json, sys, os
from datetime import datetime
from datetime import datetime
import uuid
from icalendar import Calendar, Todo
from PySide6.QtCore import QObject, Signal

class Storage(QObject):
    data_changed = Signal()  # Signal emitted when data changes

    def __init__(self):
        super().__init__()
        self.todos = []
        self.base_dir = ""

        # Определяем путь к файлу в зависимости от того, запущен ли код как release-сборка
        if getattr(sys, 'frozen', False):
            # Если код запущен как .exe
            self.base_dir = sys._MEIPASS
        else:
            # Используем текущую директорию
            self.script_directory =  os.path.dirname(os.path.abspath(__file__))
            self.base_dir = os.path.abspath(os.path.join(self.script_directory, ".."))

    # Загрузить данные из JSON
    def load_from_json(self, filename='storage.json'):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.todos = json.load(file)
        except FileNotFoundError:
            print(f'Файл {filename} не найден')
        except json.JSONDecodeError:
            print(f'Ошибка при декодировании файла {filename}')

    # Сохранить данные в JSON
    def save_to_json(self, filename='storage.json'):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.todos, file, indent=4)

    # Экспортировать данные в ICS-файл
    def export_to_ics(self, filename):
        cal = Calendar()
        cal.add('prodid', 'TodoApp')
        cal.add('version', '1.0')

        for todo in self.todos:
            ics_todo = Todo()
            ics_todo.add('uid', str(uuid.uuid4()))
            ics_todo.add('dtstamp', datetime.now())
            ics_todo.add('created', datetime.now())
            ics_todo.add('summary', todo['title'])
            ics_todo.add('description', todo.get('description', ''))

            # Преобразование статуса
            status_map = {'overdue': 'NEEDS-ACTION', 'completed': 'COMPLETED'}
            ics_todo.add('status', status_map.get(todo['status'], 'NEEDS-ACTION'))

            # Дата и время выполнения задачи
            due_date = datetime.strptime(
                f"{todo['date']} {todo['time']}",
                "%d.%m.%Y %H:%M"
            )
            ics_todo.add('due', due_date)

            cal.add_component(ics_todo)

        with open(filename, 'wb') as f:
            f.write(cal.to_ical())

    # Импортировать данные из ICS-файла
    def import_from_ics(self, filename):
        with open(filename, 'rb') as f:
            cal = Calendar.from_ical(f.read())
            self.todos = []

            for component in cal.walk():
                if component.name == 'VTODO':
                    # Извлечение данных
                    title = component.get('summary', 'Без названия')
                    description = component.get('description', '')
                    status = str(component.get('status', 'NEEDS-ACTION'))
                    due = component.get('due')

                    # Определение даты и времени
                    if due:
                        dt = due.dt
                    else:
                        dt = component.get('dtstart').dt

                    if isinstance(dt, datetime):
                        date_str = dt.strftime("%d.%m.%Y")
                        time_str = dt.strftime("%H:%M")
                    else:
                        date_str = dt.strftime("%d.%m.%Y")
                        time_str = "00:00"

                    # Преобразование статуса обратно
                    status_map = {'NEEDS-ACTION': 'overdue', 'COMPLETED': 'completed'}
                    internal_status = status_map.get(status, 'overdue')

                    self.todos.append({
                        'title': str(title),
                        'description': str(description),
                        'status': internal_status,
                        'date': date_str,
                        'time': time_str
                    })
            self.save_to_json()

global_storage = Storage()