from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


# Цветной бейдж для отображения статусов задач
class Badge(QLabel):
    # Инит компонента
    def __init__(self, text, text_color="#ffffff", bg_color="#3498db"):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyle(text_color, bg_color)

    # Устанавливает стили для бейджа
    def setStyle(self, text_color, bg_color):
        self.setStyleSheet(f'''
            QLabel {{
                color: {text_color};
                background-color: {bg_color};
                font-size: 14px;
                font-weight: bold;
                padding: 2px 8px;
                border-radius: 4px;
            }}
        ''')
