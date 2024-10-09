import asyncio
from PyQt5.QtCore import QThread, pyqtSignal
from telegram_client import load_chats, load_messages, send_message_to_chat , get_user_info


class TelegramClientThread(QThread):
    chats_loaded = pyqtSignal(list)
    messages_loaded = pyqtSignal(str)
    message_sent = pyqtSignal(bool)
    user_info_loaded = pyqtSignal(dict)  # Новый сигнал для информации о пользователе

    def __init__(self, session_name, chat_id=None, message_count=1, message_text=None):
        super().__init__()
        self.session_name = session_name
        self.chat_id = chat_id
        self.message_count = message_count
        self.message_text = message_text

    def run(self):
        asyncio.run(self.main_task())

    async def main_task(self):
        if self.message_text:
            print(f"Sending message: {self.message_text}")
            success = await send_message_to_chat(self.session_name, self.chat_id, self.message_text)
            print(f"Message sent status: {success}")
            self.message_sent.emit(success)
        elif self.chat_id:
            print(f"Loading messages for chat_id: {self.chat_id}")
            messages = await load_messages(self.session_name, self.chat_id, self.message_count)
            print(f"Loaded messages: {messages}")
            self.messages_loaded.emit(messages)
        else:
            print(f"Loading chats for session: {self.session_name}")
            chats = await load_chats(self.session_name)
            print(f"Loaded chats: {chats}")
            self.chats_loaded.emit(chats)

            # Получаем информацию о пользователе
            print("Loading user info...")
            user_info = await get_user_info(self.session_name)
            if user_info:
                print(f"Loaded user info: {user_info}")
                self.user_info_loaded.emit({
                    'first_name': user_info.first_name,
                    'username': user_info.username,
                    'phone_number': user_info.phone_number
                })

