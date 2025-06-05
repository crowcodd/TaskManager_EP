from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QTextEdit, QComboBox, QDateTimeEdit, QPushButton, QMessageBox,
    QCheckBox, QWidget)
from PySide6.QtCore import QDateTime

class TaskCreateWindow(QDialog):
    # Инициализация компонента
    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)
        self.task_data = task_data
        self.setWindowTitle("Редактирование задачи" if task_data else "Добавление задачи")
        self.setModal(True)
        self.create_ui()
        
        if self.task_data:
            self.fill_form_data()

    # Создать диалоговое окно
    def create_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Поле для ввода названия задачи
        title_layout = QHBoxLayout()
        title_label = QLabel("Назовите задачу")
        self.title_input = QLineEdit()
        self.title_input.setMaxLength(100)
        self.title_length_label = QLabel("0/100")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        title_layout.addWidget(self.title_length_label)
        layout.addLayout(title_layout)

        # Проверка на вводимые символы в поле Название
        self.title_input.textChanged.connect(self.update_title_length)

        # Поле для ввода описания задачи
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Дополнительная информация о задаче")
        self.desc_input = QTextEdit()
        self.desc_length_label = QLabel("0/500")
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        desc_layout.addWidget(self.desc_length_label)
        layout.addLayout(desc_layout)

        # Проверка на вводимые символы в поле Описание
        self.desc_input.textChanged.connect(self.update_desc_length)

        # Список возможных статусов
        status_layout = QHBoxLayout()
        status_label = QLabel("Статус задачи")
        self.status_dropdown = QComboBox()
        self.status_dropdown.addItems(["Ожидает", "В процессе", "Выполнена"])
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_dropdown)
        layout.addLayout(status_layout)

        # Чекбокс для включения/выключения даты
        self.use_datetime_checkbox = QCheckBox("Хочу указать дату и время")
        self.use_datetime_checkbox.setChecked(True)
        self.use_datetime_checkbox.stateChanged.connect(self.toggle_datetime)
        layout.addWidget(self.use_datetime_checkbox)

        # Поле для даты и времени
        self.datetime_container = QWidget()
        datetime_layout = QHBoxLayout(self.datetime_container)
        datetime_label = QLabel("Крайний срок выполнения (дедлайн)")
        self.datetime_input = QDateTimeEdit()
        
        # Устанавливаем дату по умолчанию (текущая + 1 день)
        default_datetime = QDateTime.currentDateTime().addDays(1)
        self.datetime_input.setDateTime(default_datetime)
        self.datetime_input.setCalendarPopup(True)
        
        datetime_layout.addWidget(datetime_label)
        datetime_layout.addWidget(self.datetime_input)
        layout.addWidget(self.datetime_container)

        # Кнопки
        layout_btns = QVBoxLayout()
        save_btn_text = "Добавить задачу"
        if self.task_data:
            save_btn_text = "Сохранить изменения"
        
        self.save_btn = QPushButton(save_btn_text)
        layout_btns.addWidget(self.save_btn)

        # Добавляем новые кнопки только для режима редактирования
        if self.task_data:
            self.complete_btn = QPushButton("Отметить как выполненное")
            self.delete_btn = QPushButton("Удалить")
            layout_btns.addWidget(self.complete_btn)
            layout_btns.addWidget(self.delete_btn)

            # Задаём стили для кнопок
            self.complete_btn.setStyleSheet("""
            QPushButton {
                border-radius: 16px;
                padding: 6px 12px;
                background-color: #E1E0E0;
                font-size: 18px;
                color: black;
            }
            """)
            
            self.delete_btn.setStyleSheet("""
            QPushButton {
                border-radius: 16px;
                padding: 6px 12px;
                background-color: #E1E0E0;
                font-size: 18px;
                color: black;
            }
            """)
            
            # Обработчики кнопок
            self.complete_btn.clicked.connect(self.mark_as_completed)
            self.delete_btn.clicked.connect(self.delete_task)

        layout.addLayout(layout_btns)

        # Обработчик для кнопки сохранения
        self.save_btn.clicked.connect(self.validate_fields)

    # Обновить количество введённых символов в поле Название
    def update_title_length(self):
        length = len(self.title_input.text())
        self.title_length_label.setText(f"{length}/100")
        self.title_length_label.setStyleSheet("color: red;" if length == 100 else "color: black;")

    # Обновить количество введённых символов в поле Описание
    def update_desc_length(self):
        text = self.desc_input.toPlainText()
        if len(text) > 500:
            # Обрезаем текст и обновляем поле
            self.desc_input.blockSignals(True)
            self.desc_input.setPlainText(text[:500])
            self.desc_input.blockSignals(False)
            self.desc_length_label.setText("500/500")
            self.desc_length_label.setStyleSheet("color: red;")
        else:
            self.desc_length_label.setText(f"{len(text)}/500")
            self.desc_length_label.setStyleSheet("color: red;" if len(text) == 500 else "color: black;")

    # Показать/скрыть поле для даты и времени
    def toggle_datetime(self, state):
        self.datetime_container.setVisible(state)
        
    # Загрузить данные из задачи в форму
    def fill_form_data(self):
        # Обрезаем данные при загрузке, если необходимо
        title = self.task_data['title'][:100]
        self.title_input.setText(title)
        
        desc = self.task_data['description'][:500]
        self.desc_input.setText(desc)
        
        # slug статуса -> Текст
        status_text = "Ожидает"
        if self.task_data['status'] == "created":
            status_text = "В процессе"
        elif self.task_data['status'] == "completed":
            status_text = "Выполнена"
        
        # Ищем статус по индексу    
        index = self.status_dropdown.findText(status_text)
        if index >= 0:
            self.status_dropdown.setCurrentIndex(index)
            
        # Загружаем дату и время если они есть
        if self.task_data['date'] and self.task_data['time']:
            datetime_str = f"{self.task_data['date']} {self.task_data['time']}"
            datetime = QDateTime.fromString(datetime_str, "dd.MM.yyyy HH:mm")
            self.datetime_input.setDateTime(datetime)
            self.use_datetime_checkbox.setChecked(True)
        else:
            self.use_datetime_checkbox.setChecked(False)

    # Получить данные формы
    def get_task_data(self):
        data = {
            'title': self.title_input.text(),
            'description': self.desc_input.toPlainText(),
            'status': self.status_dropdown.currentText(),
        }
        
        # Добавляем дату и время, только если включен чекбокс
        if self.use_datetime_checkbox.isChecked():
            data.update({
                'date': self.datetime_input.dateTime().toString("dd.MM.yyyy"),
                'time': self.datetime_input.dateTime().toString("HH:mm")
            })
        else:
            data.update({
                'date': "",
                'time': ""
            })
            
        return data

    # Пометить задачу отмеченной
    def mark_as_completed(self):
        self.status_dropdown.setCurrentText("Выполнена")
        self.accept()

    # Удалить задачу
    def delete_task(self):
        self.done(-1)

    # Проверка полей
    def validate_fields(self):
        errors = []
        
        # Проверка заголовка
        if not self.title_input.text().strip():
            errors.append("Название не может быть пустым")
            
        # Проверка даты только если включен чекбокс
        if self.use_datetime_checkbox.isChecked():
            selected_datetime = self.datetime_input.dateTime()
            current_datetime = QDateTime.currentDateTime()
            
            if selected_datetime < current_datetime:
                errors.append("Дата и время не могут быть в прошлом")
            
        # Если есть ошибки - показываем их
        if errors:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Ошибка валидации")
            error_message.setText(f"Пожалуйста, исправьте следующие ошибки:\n\n{'\n'.join(errors)}")
            error_message.exec()
            return
            
        super().accept()