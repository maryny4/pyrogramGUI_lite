from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QSplitter, QPushButton, QComboBox, QHBoxLayout, \
    QLineEdit, QToolButton, QScrollArea, QSizePolicy, QFileDialog
from PyQt5.QtCore import Qt, QSize,QRect
from PyQt5.QtGui import QPainter, QColor, QFont,QFontMetrics
from threads import TelegramClientThread
import os
from PyQt5.QtCore import QTimer


class MessageBubble(QWidget):
    def __init__(self, text, timestamp, is_sender=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.timestamp = timestamp
        self.is_sender = is_sender

        # Устанавливаем минимальный размер пузырька
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Цвета для отправителя и получателя
        self.sender_color = QColor(0, 92, 153)  # Синий фон для отправителя
        self.receiver_color = QColor(43, 43, 43)  # Серый фон для получателя
        self.text_color = QColor(255, 255, 255)  # Белый цвет текста

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Цвет пузырька в зависимости от отправителя/получателя
        if self.is_sender:
            bubble_color = self.sender_color
            align = Qt.AlignRight  # Отправитель - справа
        else:
            bubble_color = self.receiver_color
            align = Qt.AlignLeft  # Получатель - слева

        # Рисуем пузырек
        painter.setBrush(bubble_color)
        painter.setPen(Qt.NoPen)
        rect = QRect(10, 10, self.width() - 20, self.height() - 20)
        painter.drawRoundedRect(rect, 15, 15)

        # Шрифт для текста сообщения
        painter.setFont(QFont("Arial", 12))

        # Рисуем текст сообщения
        painter.setPen(self.text_color)
        text_rect = QRect(20, 20, self.width() - 40, self.height() - 50)  # Отступы для текста
        painter.drawText(text_rect, Qt.TextWordWrap | align, self.text)

        # Шрифт для времени
        painter.setFont(QFont("Arial", 8))
        painter.setPen(QColor(192, 192, 192))

        # Рисуем время сообщения
        timestamp_rect = QRect(20, self.height() - 30, self.width() - 40, 20)  # Отступы для времени
        painter.drawText(timestamp_rect, align, self.timestamp)

    def sizeHint(self):
        # Используем QFontMetrics для расчёта высоты текста
        font = QFont("Arial", 12)  # Шрифт для текста
        font_metrics = QFontMetrics(font)

        # Рассчитываем высоту текста с учетом ширины пузырька
        text_width = self.width() - 40  # Ширина, оставшаяся для текста с учетом отступов
        text_height = font_metrics.boundingRect(QRect(0, 0, text_width, 0), Qt.TextWordWrap, self.text).height()

        # Добавляем высоту для времени и отступы
        bubble_height = text_height + 50  # Увеличиваем высоту для текста и времени
        return QSize(200, bubble_height)  # Минимальный размер пузырька


class TelegramApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Single-Session Chat Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.current_user_name = "ME"

        layout = QVBoxLayout(self)

        # Header section
        header_layout = QHBoxLayout()
        self.session_label = QLabel("Selected session: None")
        self.select_session_button = QToolButton()
        self.select_session_button.setText("Select Session")
        self.select_session_button.clicked.connect(self.select_session)

        self.refresh_button = QToolButton()
        self.refresh_button.setText("Refresh")
        self.refresh_button.clicked.connect(self.refresh_messages)

        # User info label (added back)
        self.user_info_label = QLabel("User Info: Not Loaded")
        self.user_info_label.setAlignment(Qt.AlignRight)
        header_layout.addWidget(self.session_label)
        header_layout.addWidget(self.select_session_button)
        header_layout.addWidget(self.refresh_button)
        header_layout.addWidget(self.user_info_label)
        layout.addLayout(header_layout)

        # Chat list and message viewer
        self.chat_list = QListWidget()
        self.message_area = QScrollArea()
        self.message_area.setWidgetResizable(True)

        self.message_widget = QWidget()
        self.message_layout = QVBoxLayout(self.message_widget)
        self.message_area.setWidget(self.message_widget)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.chat_list)
        splitter.addWidget(self.message_area)
        layout.addWidget(splitter)

        # Message count selector
        message_count_layout = QHBoxLayout()
        self.message_count_selector = QComboBox()
        self.message_count_selector.addItems(["1", "5", "10", "20", "50", "100"])
        message_count_layout.addWidget(QLabel("Number of messages to load:"))
        message_count_layout.addWidget(self.message_count_selector)
        layout.addLayout(message_count_layout)

        # Message input and send button
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter your message here...")

        self.send_message_button = QToolButton()
        self.send_message_button.setText("Send")
        self.send_message_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_message_button)
        layout.addLayout(input_layout)

        # Chat list selection connection
        self.chat_list.itemClicked.connect(self.show_latest_messages)

        # Data storage
        self.chat_data = {}
        self.selected_session = None
        self.current_thread = None
        self.current_chat_id = None

        # Apply styles after all elements have been created
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QListWidget, QTextBrowser, QLineEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #3a3a3a;
            }
            QToolButton {
                background-color: #3a8dda;
                color: #ffffff;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
            QToolButton:hover {
                background-color: #357ab7;
            }
            QToolButton:pressed {
                background-color: #2c6aa1;
            }
            QSplitter::handle {
                background-color: #3a8dda;
            }
            QLabel {
                color: #b0b0b0;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background-color: #2a2a2a;
                width: 16px;
                margin: 16px 0 16px 0;
            }
            QScrollBar::handle:vertical {
                background-color: #4a4a4a;
                min-height: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3a8dda;
            }
        """)
        self.select_session_button.setStyleSheet("""
            QToolButton {
                background-color: #3a8dda;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 20px;
                border: none;
            }
            QToolButton:hover {
                background-color: #357ab7;
            }
            QToolButton:pressed {
                background-color: #2c6aa1;
            }
        """)
        self.send_message_button.setStyleSheet("""
            QToolButton {
                background-color: #4caf50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 20px;
                border: none;
            }
            QToolButton:hover {
                background-color: #43a047;
            }
            QToolButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.chat_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #4caf50;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3a8dda;
                color: white;
            }
        """)

    def select_session(self):
        session_file, _ = QFileDialog.getOpenFileName(self, "Select session file", "sessions",
                                                      "Session Files (*.session)")
        if session_file:
            self.selected_session = os.path.splitext(session_file)[0]
            self.session_label.setText(f"Selected session: {os.path.basename(self.selected_session)}")
            self.load_chats()

    def load_chats(self):
        if not self.selected_session:
            return
        self.set_ui_enabled(False)

        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.terminate()
            self.current_thread.wait()

        self.current_thread = TelegramClientThread(self.selected_session)
        self.current_thread.chats_loaded.connect(self.load_chats_to_ui)
        self.current_thread.user_info_loaded.connect(self.update_user_info)  # Connect user info signal
        self.current_thread.finished.connect(self.on_loading_finished)
        self.current_thread.start()

    def set_ui_enabled(self, enabled):
        self.chat_list.setEnabled(enabled)
        self.select_session_button.setEnabled(enabled)
        self.refresh_button.setEnabled(enabled)
        self.send_message_button.setEnabled(enabled)
        self.message_input.setEnabled(enabled)
        self.message_count_selector.setEnabled(enabled)

    def on_loading_finished(self):
        self.set_ui_enabled(True)

    def load_chats_to_ui(self, chats):
        self.chat_list.clear()
        self.chat_data.clear()
        for chat_title, chat_id in chats:
            self.chat_list.addItem(f"{chat_title} (ID: {chat_id})")
            self.chat_data[chat_id] = None

    def update_user_info(self, user_info):
        """Обновляем метку с информацией о пользователе и сохраняем имя текущего пользователя"""
        print(f"User info received: {user_info}")  # Вывод данных о пользователе для проверки

        # Получаем first_name, username и другие данные
        first_name = user_info.get('first_name', 'Unknown')
        username = user_info.get('username', 'No username')
        phone = user_info.get('phone_number', 'No phone')

        # Сохраняем first_name текущего пользователя в атрибуте класса
        self.current_user_first_name = first_name  # <--- Теперь атрибут инициализирован

        # Обновляем информацию в интерфейсе
        self.user_info_label.setText(f"User: {first_name} (@{username}) | Phone: {phone}")

    def show_latest_messages(self, item):
        chat_info = item.text()
        chat_id = int(chat_info.split("ID: ")[1].strip(')'))
        self.current_chat_id = chat_id
        message_count = int(self.message_count_selector.currentText())

        # Clear previous messages from the layout
        for i in reversed(range(self.message_layout.count())):
            widget = self.message_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.chat_data[chat_id] = None

        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.terminate()
            self.current_thread.wait()

        self.current_thread = TelegramClientThread(self.selected_session, chat_id=chat_id, message_count=message_count)
        self.current_thread.messages_loaded.connect(self.display_messages)
        self.current_thread.start()

    # Прокрутите до последнего сообщения напрямую
    from PyQt5.QtCore import QTimer

    def display_messages(self, messages):
        try:
            # Очищаем старые сообщения
            for i in reversed(range(self.message_layout.count())):
                widget = self.message_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            # Добавляем новые сообщения
            last_message_bubble = None
            for message in reversed(messages.splitlines()):
                parts = message.split(' - ', 1)
                if len(parts) < 2:
                    continue

                if ': ' in parts[1]:
                    sender_info, text = parts[1].split(': ', 1)
                else:
                    sender_info = parts[1]
                    text = ""

                sender_info = sender_info.strip()
                timestamp = parts[0].strip()

                is_sender = sender_info == self.current_user_first_name.strip()

                bubble = MessageBubble(text, timestamp, is_sender=is_sender)
                self.message_layout.addWidget(bubble)
                last_message_bubble = bubble

            self.message_layout.addStretch()

            # Прокрутка до последнего сообщения после небольшого таймаута
            QTimer.singleShot(100, self.scroll_to_bottom)

        except Exception as e:
            print(f"Error processing messages: {e}")

    def scroll_to_bottom(self):
        """Метод для прокрутки области сообщений вниз"""
        scrollbar = self.message_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def refresh_messages(self):
        """Обновляет сообщения в текущем чате"""
        current_item = self.chat_list.currentItem()
        if current_item:
            self.show_latest_messages(current_item)


    def send_message(self):
        if not self.current_chat_id:
            return

        message_text = self.message_input.text().strip()
        if not message_text:
            return

        self.message_input.clear()

        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.terminate()
            self.current_thread.wait()

        self.current_thread = TelegramClientThread(self.selected_session, chat_id=self.current_chat_id,
                                                   message_text=message_text)
        self.current_thread.message_sent.connect(self.message_sent_confirmation)
        self.current_thread.start()

    def message_sent_confirmation(self):
        """Обработка события после успешной отправки сообщения"""
        print("Message sent successfully!")

        # Обновление сообщений в текущем чате после отправки
        self.refresh_messages()  # This will call show_latest_messages for the current chat.