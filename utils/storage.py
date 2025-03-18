import json, sys, os

class Storage:
    def __init__(self):
        self.todos = []
        self.base_dir = ""

        # Определяем путь к файлу в зависимости от того, запущен ли код как .exe
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

    # Экспортировать данные в .TSK
    def export_to_tsk(self, filename):
        self.save_to_json(filename)

    # Импорт из .TSK
    def import_from_tsk(self, filename):
        self.load_from_json(filename)

    # Добавить задачу в список
    def add_todo(self, todo):
        self.todos.append(todo)
        self.save_to_json()

global_storage = Storage()