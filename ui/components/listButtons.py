from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton, QFileDialog
from PySide6.QtCore import QSize

from utils.storage import global_storage

# Кнопки над списком задач
class ListButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Создаём Layout
        layout = QHBoxLayout()

        # Иконка для кнопки экспорта
        export_icon = QIcon(f"{global_storage.base_dir}/resources/icons/upload.svg")

        # Создаём кнопку экспорта
        self.export_btn = QPushButton(export_icon, "Экспорт")
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_tasks_dialog)
        self.export_btn.setIconSize(QSize(28, 18))

        # Иконка для кнопки импорта
        import_icon = QIcon(f"{global_storage.base_dir}/resources/icons/download.svg")

        # Создаём кнопку импорта
        self.import_btn = QPushButton(import_icon, "Импорт")
        self.import_btn.setCursor(Qt.PointingHandCursor)
        self.import_btn.clicked.connect(self.import_tasks_dialog)
        self.import_btn.setIconSize(QSize(28, 18))

        # Добавляем заголовок в layout
        layout.addWidget(self.export_btn)
        layout.addWidget(self.import_btn)
        self.setLayout(layout)

    # Диалог экспорта задач
    def export_tasks_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Экспорт задач", "save.tsk", "Файл .tsk (*.tsk)", options=options)
        if file_name:
            global_storage.export_to_tsk(file_name)

    # Диалог импорта задач
    def import_tasks_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Импорт задач", "", "Файл .tsk (*.tsk)", options=options)
        if file_name:
            global_storage.import_from_tsk(file_name)