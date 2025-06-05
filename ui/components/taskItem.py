from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter, QColor
from .badge import Badge
from .svgIcon import SvgIconWidget
from utils.storage import global_storage

# Элемент задачи для списка
class TaskCardV2(QWidget):
    def __init__(self, title, description, status, time = "", date = ""):
        super().__init__()

        # Создаём Layout
        layout = QVBoxLayout()

        # Создаём блок заголовка
        header = QHBoxLayout()

        # Добавляем в хидер заголовок
        header_title = QLabel(title)
        header_title.setStyleSheet("""
            QLabel {
                font-weight: 800;
                font-size: 16pt;
            }
        """)
        header.addWidget(header_title)

        # Добавляем в хидер галочку
        double_mark = QLabel()

        # Загружаем SVG-иконку
        svg_renderer = QSvgRenderer(f"{global_storage.base_dir}/resources/icons/check-check.svg")
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        double_mark.setPixmap(pixmap)

        double_mark.setStyleSheet("""
            QLabel {
                color: rgb(200,200,200);
                font-size: 32px;
            }
        """)
        double_mark.setFixedSize(32, 32)
        if status == "completed":
            header.addWidget(double_mark)

        # Создаём описание
        description = QLabel(description)
        description.setStyleSheet("""
            QLabel {
                font-size: 15pt;
            }
        """)

        # Создаём список с отметками статуса
        badges_list = QHBoxLayout()
        badges_list.setSpacing(4)
        if status == "completed":
            badges_list.addWidget(Badge("Выполнена", "#919191", "#d2d2d2"))
        if status == "created":
            badges_list.addWidget(Badge("Ожидает", "#e3af2a", "#f5e1ad"))
        if status == "overdue":
            badges_list.addWidget(Badge("Просрочена", "#cf1d1d", "#caa0a0"))

        badges_list.addStretch()

        # Создаём layout для даты и времени
        datetime_layout = QHBoxLayout()
        datetime_layout.setSpacing(4)

        # Создаём дату и время
        if time:
            time_icon = SvgIconWidget(f"{global_storage.base_dir}/resources/icons/clock.svg", 20, 20)

            time_label = QLabel(time)
            time_label.setStyleSheet("QLabel {font-size: 14px;}")
            time_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            datetime_layout.addWidget(time_icon)
            datetime_layout.addWidget(time_label)

        if date:
            date_icon = SvgIconWidget(f"{global_storage.base_dir}/resources/icons/calendar.svg", 20, 20)

            date_label = QLabel(date)
            date_label.setStyleSheet("QLabel {font-size: 14px;}")

            datetime_layout.addWidget(date_icon)
            datetime_layout.addWidget(date_label)

        # Добавляем header в layout
        layout.addLayout(header)
        layout.addWidget(description)
        if date or time:
            layout.addLayout(datetime_layout)
        layout.addLayout(badges_list)
        self.setStyleSheet("""
                           QVBoxLayout:focus {
                           background: red;
                           }
                           """)
        self.setLayout(layout)
