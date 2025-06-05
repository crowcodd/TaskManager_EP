from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QDialog, QListWidgetItem
from PySide6.QtCore import QSize
from datetime import datetime

from .taskItem import TaskCardV2
from .taskCreateWindow import TaskCreateWindow
from utils.storage import global_storage

# Столбец списка задач
class KanbanColumn(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Загружаем данные из хранилища
        global_storage.load_from_json()

        # Список задач
        self.task_list = QListWidget()

        # Задаём фоновый цвет для нажатой задачи
        self.task_list.setStyleSheet("""
            QListWidget::item:selected {
                background: rgba(109,137,132,0.5);
            }""")        

        # Кнопки
        self.buttons_wrapper = QHBoxLayout()

        # Иконка для кнопки добавления задачи
        add_icon = QIcon(f"{global_storage.base_dir}/resources/icons/plus.svg")

        # Кнопка добавления задач
        add_button = QPushButton(add_icon, "Добавить задачу")
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.clicked.connect(self.show_create_task_dialog)
        add_button.setIconSize(QSize(21, 21))

        # Добавляем кнопку в wrapper
        self.buttons_wrapper.addWidget(add_button)

        # Double click: Редактирование задачи
        self.task_list.itemDoubleClicked.connect(self.on_task_double_clicked)

        layout.addWidget(self.task_list)
        layout.addLayout(self.buttons_wrapper)
        self.setLayout(layout)

    # Показать диалог создания задачиAdd commentMore actions
    def show_create_task_dialog(self):
        dialog = TaskCreateWindow(self)
        if dialog.exec() == QDialog.Accepted:
            # Получаем данные из диалога
            task_data = dialog.get_task_data()

            # Получаем slug для статуса
            status = ""
            match task_data['status']:
                case "Ожидает":
                    status = "created"
                case "В процессе":
                    status = "created"
                case "Завершён":
                    status = "completed"

            # Сохраняем задачи
            global_storage.todos.append({
                'title': task_data['title'],
                'description': task_data['description'],
                'status': status,
                'time': task_data['time'],
                'date': task_data['date']
            })
            global_storage.save_to_json()

            # Обновляем список задач
            self.load_from_storage()

    # Добавить задачу
    def add_task(self, title, description, status, time = "", date = ""):
        task_widget = TaskCardV2(title, description, status, time, date)
        list_item = QListWidgetItem(self.task_list)

        list_item.setSizeHint(task_widget.sizeHint())
        self.task_list.addItem(list_item)
        self.task_list.setItemWidget(list_item, task_widget)

    # Очистить список
    def clear_tasks(self):
        self.task_list.clear()

    # Загрузить задачи из файла
    def load_from_storage(self):
        self.clear_tasks()
        for task in global_storage.todos:
            self.check_overdue_status(task)
            self.add_task(task['title'], task['description'], task['status'], task['time'] or "", task['date'] or "")
        global_storage.save_to_json()  # Сохраняем обновленные статусы

    # При двойном клике на задачу
    def on_task_double_clicked(self, item):
        self.edit_task(self.task_list.row(item))

    # Открыть задачу для редактирования
    def edit_task(self, task_index):
        if task_index >= 0 and task_index < len(global_storage.todos):
            task_data = global_storage.todos[task_index]
            dialog = TaskCreateWindow(self, task_data)
            
            result = dialog.exec()
            if result == QDialog.Accepted:
                # Получаем обновлённые данные
                updated_data = dialog.get_task_data()
                
                # Статус -> slug
                status = ""
                match updated_data['status']:
                    case "Ожидает":
                        status = "created"
                    case "В процессе":    
                        status = "created"
                    case "Выполнена":    
                        status = "completed"
                
                # Обновляем данные в хранилище
                global_storage.todos[task_index].update({
                    'title': updated_data['title'],
                    'description': updated_data['description'],
                    'status': status,
                    'time': updated_data['time'],
                    'date': updated_data['date']
                })
                global_storage.save_to_json()
            elif result == -1:  # Проверяем на удаление
                global_storage.todos.pop(task_index)
                global_storage.save_to_json()
                
            # Перезагружаем список
            self.load_from_storage()

    # Проверка, что время на выполнение задачи ещё не истекло
    def check_overdue_status(self, task):
        if task['status'] != 'completed' and task['date'] and task['time']:
            # Генерируем строку даты для сравнения
            task_datetime_str = f"{task['date']} {task['time']}"
            # Парсинг даты из строки по формату
            task_datetime = datetime.strptime(task_datetime_str, "%d.%m.%Y %H:%M")
            if task_datetime < datetime.now():
                task['status'] = 'overdue'