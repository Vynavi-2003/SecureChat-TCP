import socket
import threading
import json
from cryptography.fernet import Fernet
import datetime

# Load encryption key
with open("secret.key", "rb") as key_file:
    secret_key = key_file.read()
cipher_suite = Fernet(secret_key)

# Server setup
host = "127.0.0.1"
port = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = {}

print("✅ Server has started on port 5555")

# --- Broadcast message to all ---
def broadcast(message, exclude_client=None):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(full_message + "\n")
    encrypted = cipher_suite.encrypt(full_message.encode())
    for client in clients:
        if client != exclude_client:
            try:
                client.send(encrypted)
            except:
                remove_client(client)

# --- Send updated user list ---
def send_user_list():
    active_users = list(usernames.values())
    payload = json.dumps({"type": "user_list", "users": active_users})
    encrypted = cipher_suite.encrypt(payload.encode())
    for client in clients:
        try:
            client.send(encrypted)
        except:
            remove_client(client)

# --- Handle each client ---
def handle_client(client):
    try:
        encrypted_username = client.recv(1024)
        username = cipher_suite.decrypt(encrypted_username).decode()
    except:
        return

    clients.append(client)
    usernames[client] = username

    broadcast(f"✅ {username} joined the chat!", exclude_client=client)
    send_user_list()

    while True:
        try:
            msg = client.recv(4096)
            decrypted_msg = cipher_suite.decrypt(msg).decode()
            broadcast(f"{username}: {decrypted_msg}")
        except:
            break

    remove_client(client)

# --- Remove disconnected client ---
def remove_client(client):
    if client in clients:
        clients.remove(client)
        left_user = usernames.pop(client, None)
        if left_user:
            broadcast(f"❌ {left_user} left the chat")
            send_user_list()

# --- Accept clients ---
def accept_connections():
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

accept_connections()