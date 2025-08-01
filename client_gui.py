import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from cryptography.fernet import Fernet
import datetime
import json

# Load encryption key
with open("secret.key", "rb") as key_file:
    secret_key = key_file.read()
cipher_suite = Fernet(secret_key)

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

username = ""

# GUI setup
root = tk.Tk()
root.withdraw()  # Hide main window until username is entered

emoji_list = ["😀", "😁", "😅", "😂", "😊", "😇", "😎", "🤔", "😢", "😡", "❤️", "👍", "👋", "🙌", "🎉"]

# --- Display Message in Chat Area ---
def display_message(message):
    chat_area.config(state="normal")
    chat_area.insert(tk.END, message + "\n")
    chat_area.yview(tk.END)
    chat_area.config(state="disabled")

# --- Update User List ---
def update_user_list(users):
    user_listbox.delete(0, tk.END)
    user_listbox.insert(tk.END, "Active Users")
    for user in users:
        user_listbox.insert(tk.END, user)

# --- Receive Messages ---
def receive_messages():
    while True:
        try:
            encrypted_msg = client.recv(4096)
            decrypted_msg = cipher_suite.decrypt(encrypted_msg).decode()

            if decrypted_msg.startswith('{"type":'):
                data = json.loads(decrypted_msg)
                if data.get("type") == "user_list":
                    update_user_list(data.get("users", []))
            else:
                display_message(decrypted_msg)
        except Exception as e:
            print("[Error receiving]:", e)
            break

# --- Send Message ---
def send_message(event=None):
    msg = msg_entry.get().strip()
    if msg:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {username}: {msg}"
        encrypted_msg = cipher_suite.encrypt(full_msg.encode())
        client.send(encrypted_msg)
        msg_entry.delete(0, tk.END)

# --- Add Emoji to Entry ---
def add_emoji(emoji):
    current_text = msg_entry.get()
    msg_entry.delete(0, tk.END)
    msg_entry.insert(0, current_text + emoji)

# --- Start Chat Window ---
def start_chat_window():
    global chat_area, msg_entry, user_listbox

    root.deiconify()
    root.title("Secure TCP Chat")
    root.geometry("750x550")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    chat_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state="disabled")
    chat_area.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

    user_listbox = tk.Listbox(main_frame, width=20)
    user_listbox.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)
    user_listbox.insert(tk.END, "Active Users")

    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X, padx=5, pady=5)

    msg_entry = tk.Entry(input_frame, font=("Arial", 14))
    msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    msg_entry.bind("<Return>", send_message)

    send_btn = tk.Button(input_frame, text="Send", command=send_message)
    send_btn.pack(side=tk.RIGHT, padx=5)

    emoji_frame = tk.Frame(root)
    emoji_frame.pack(fill=tk.X, padx=5, pady=3)
    for emoji in emoji_list:
        b = tk.Button(emoji_frame, text=emoji, font=("Arial", 12), width=2, command=lambda e=emoji: add_emoji(e))
        b.pack(side=tk.LEFT, padx=1)

    threading.Thread(target=receive_messages, daemon=True).start()

# --- Username Prompt ---
def submit_username(event=None):
    global username
    username = username_entry.get().strip()
    if username:
        try:
            encrypted_username = cipher_suite.encrypt(username.encode())
            client.send(encrypted_username)
            username_prompt.destroy()
            start_chat_window()
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

username_prompt = tk.Toplevel()
username_prompt.title("Enter Username")
username_prompt.geometry("300x100")

username_entry = tk.Entry(username_prompt, font=("Arial", 14))
username_entry.pack(pady=10)
username_entry.focus()
username_entry.bind("<Return>", submit_username)

submit_btn = tk.Button(username_prompt, text="Submit", command=submit_username)
submit_btn.pack()

root.mainloop()
