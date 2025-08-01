# 🔐 Secure TCP Chat Application (Client-Server) with GUI, Emoji & Encryption

This is a real-time chat application built using Python. It uses **TCP sockets** for communication, **Tkinter** for the graphical user interface, and **Fernet symmetric encryption** from the `cryptography` library to ensure secure message transfer.

✅ Chat like WhatsApp with:
- Emoji support  
- Real-time messages  
- Active user list  
- Timestamped logs  
- Encrypted communication  
- User join/leave alerts

---

## 🗂️ Features

### ✅ Server Side (`server.py`)
- Handles multiple clients with threads.
- Sends encrypted messages using Fernet.
- Broadcasts messages to all clients.
- Maintains an **active user list**.
- Logs all chat history in `chat_log.txt`.

### 💬 Client Side (`client_gui.py`)
- GUI chat window with:
  - Chat area
  - Emoji panel
  - Message input field
  - Active users sidebar
- Prompts for username on startup.
- Messages are encrypted and timestamped.
- Displays join/leave notifications.

---

## 🛠️ Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```
Required libraries:
- cryptography
- tkinter (comes pre-installed with Python)

### 🔐 Encryption
Uses Fernet symmetric encryption.

A secret.key is generated using generate_key.py.

All messages (including usernames) are encrypted before being sent.

Run once to generate the encryption key:

```bash
python generate_key.py
```
###🚀 How to Run
Generate encryption key:

```bash
python generate_key.py
```
Start the server:

```bash
python server.py
```
Start one or more clients:

```bash
python client_gui.py
```
Enter a username in the popup to begin chatting.

### 📁 Project Structure
```bash
📁 Secure-TCP-Chat/
├── server.py              # Server-side logic
├── client_gui.py          # GUI chat client
├── generate_key.py        # Key generator
├── secret.key             # Symmetric encryption key (generated)
├── chat_log.txt           # Log of all chat messages
├── requirements.txt       # Python dependencies
└── README.md              # Project overview
```
### 💡 Example
```bash
# In terminal 1
python server.py
✅ Server has started on port 5555

# In terminal 2
python client_gui.py
✅ vyn joined the chat!

# In terminal 3
python client_gui.py
✅ tom joined the chat!
```

Chat messages will look like:

```csharp
[21:19:56] vyn: hello!!
[21:20:57] ✅ tom joined the chat!
[21:21:03] tom: hello vyn
[21:22:31] vyn: 😀 ntg
```
### 💬 Emojis Supported
😀 😁 😅 😂 😊 😇 😎 🤔 😢 😡 ❤️ 👍 👋 🙌 🎉

