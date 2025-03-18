from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget

class AppTitle(QWidget):
    def __init__(self):
        super().__init__()

        # Создаём Layout
        layout = QVBoxLayout()

        # Создаём заголовок
        self.label = QLabel("Менеджер задач")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('''
                                 QLabel {
                                 font-size: 32px;
                                 font-weight: normal;}
                                 ''')

        # Добавляем заголовок в layout
        layout.addWidget(self.label)
        self.setLayout(layout)
