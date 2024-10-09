## Telegram Single-Session Chat Viewer

### Description

**Telegram Single-Session Chat Viewer** is a GUI application built using PyQt5 that allows users to interact with their Telegram chats directly through **locally stored session files** created by **Pyrogram**. The app enables users to view, manage, and send messages from their Telegram chats without relying on official web or mobile clients. The use of **Pyrogram sessions** ensures that the app operates securely and independently of other Telegram interfaces.

### Key Features

1. **View chat list**: Load and display the list of chats from a selected **Pyrogram session** file.
2. **View messages**: Display recent messages from the selected chat in a bubble-style conversation format.
3. **Send messages**: Users can send messages to the selected Telegram chat directly through the session.
4. **User information**: Display basic user information (name, username, and phone number) from the **Pyrogram session**.
5. **Session management**: Load and interact with data from a selected **Telegram session file**.
6. **Customizable message count**: Users can choose how many recent messages to load (e.g., 1, 5, 10, etc.).
7. **Automatic scrolling**: The app automatically scrolls to the latest message after loading or sending messages.

### Importance of Pyrogram Sessions

The core functionality of this app revolves around **Pyrogram session files**, which store Telegram authentication data locally. By interacting directly with these sessions, the app provides a secure and private way to access Telegram messages without requiring a login through the official client. This method ensures faster interactions and eliminates the need to re-authenticate through Telegram's servers.

### Technologies Used

- **PyQt5**: The primary library for creating the graphical user interface (GUI).
- **Pyrogram**: A Telegram API client that enables direct interaction with Telegram using session files.
- **TelegramClientThread**: Custom threading to handle asynchronous data loading from **Pyrogram sessions** without freezing the main interface.

### Installation and Setup

1. **Clone the repository** (if applicable) or download the source files.
   
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

### Main Interface Components

- **Header**: Displays the currently selected **Pyrogram session** and includes a button to load a new session.
- **Chat List**: Shows the available chats from the loaded **Telegram session file**.
- **Message Area**: Displays chat messages in a bubble format for easy reading.
- **Message Input**: A text box where users can type and send messages.
- **Message Count Selector**: Lets users choose how many messages to load (options like 1, 5, 10, 20, 50, 100).

### Style and Appearance

The app uses a modern dark theme with smooth, rounded UI elements. Buttons and list items change color on hover and click, providing a polished user experience.

### Usage Example

1. Click the "Select Session" button to load a **Pyrogram session** file.
2. Once the session is loaded, select a chat from the chat list.
3. The messages will load in the message view area, and you can type and send new messages using the input box.
4. Use the "Refresh" button to update the chat and load new messages.

### Conclusion

**Telegram Single-Session Chat Viewer** provides a simple yet powerful way to interact with Telegram messages by leveraging **Pyrogram session files**. This approach ensures secure and private access to your messages, making the app ideal for users who prefer a lightweight desktop environment for managing their Telegram chats.
