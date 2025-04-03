from PySide6.QtWidgets import QLabel
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

# Обёртка для рендеринга SVG-иконок
class SvgIconWidget(QLabel):
    def __init__(self, svg_file, width, height, parent=None):
        super().__init__(parent)
        self.svg_file = svg_file
        self.setFixedSize(width, height)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Загрузка SVG
        renderer = QSvgRenderer(self.svg_file)
        # Фон
        painter.fillRect(self.rect(), Qt.transparent)
        # Рисуем SVG и окрашиваем его
        renderer.render(painter, self.rect())