from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QFontDatabase
from ui.components.listButtons import ListButtons
from ui.components.tasksList import KanbanColumn
from ui.components.title import AppTitle
from utils.storage import global_storage
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Главный layout
        layout = QVBoxLayout()
        layout.setSpacing(0)

        # Корневые компоненты
        self.title = AppTitle()
        self.buttons = ListButtons()
        self.column = KanbanColumn()
        self.column.load_from_storage()

        # Добавляем на лэйаут
        layout.addWidget(self.title)
        layout.addWidget(self.buttons)
        layout.addWidget(self.column)

        self.setLayout(layout)
        self.setWindowTitle("Менеджер задач")

app = QApplication([])
window = MainWindow()

# Загружаем шрифт
QFontDatabase.addApplicationFont(os.path.join(global_storage.base_dir, "resources", "Mulish.ttf"))

# Загружаем стиль
with open(os.path.join(global_storage.base_dir, "styles", "global.qss"), "r") as f:
    app.setStyleSheet(f.read())

if __name__ == "__main__":
    window.show()
    window.resize(570, 680)
    app.exec()