from pyrogram import Client

# Telegram API credentials
api_id = 22081933
api_hash = "a8f80a1b2ed33b295971f7c8ddde23e6"

async def run_client(session_name):
    app = Client(session_name, api_id=api_id, api_hash=api_hash)
    async with app:
        return app

async def load_chats(session_name):
    app = await run_client(session_name)
    dialogs = []
    try:
        async with app:
            async for dialog in app.get_dialogs():
                chat_name = dialog.chat.title or dialog.chat.first_name or dialog.chat.username or "No title"
                dialogs.append((chat_name, dialog.chat.id))
    except Exception as e:
        print(f"Error loading chats: {e}")
    return dialogs

async def load_messages(session_name, chat_id, message_count=1):
    app = await run_client(session_name)
    messages = []
    try:
        async with app:
            async for message in app.get_chat_history(chat_id, limit=message_count):
                sender_name = message.sender_chat.title if message.sender_chat else message.from_user.first_name
                timestamp = message.date.strftime("%Y-%m-%d %H:%M:%S")
                if message.text:
                    messages.append(f"{timestamp} - {sender_name}: {message.text}")
                elif message.caption:
                    messages.append(f"{timestamp} - {sender_name}: {message.caption}")
                elif message.media:
                    messages.append(f"{timestamp} - {sender_name} sent media: {type(message.media).__name__}")
                else:
                    messages.append(f"{timestamp} - {sender_name} sent unknown content.")
    except Exception as e:
        print(f"Error loading messages for chat {chat_id}: {e}")
    return '\n'.join(messages)

async def send_message_to_chat(session_name, chat_id, message_text):
    app = await run_client(session_name)
    try:
        async with app:
            await app.send_message(chat_id, message_text)
            return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

async def get_user_info(session_name):
    app = await run_client(session_name)
    user_info = None
    try:
        async with app:
            user_info = await app.get_me()  # Получаем информацию о текущем пользователе
    except Exception as e:
        print(f"Error getting user info: {e}")
    return user_info

