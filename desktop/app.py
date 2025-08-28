import os, threading, shutil, datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox
from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

# ---------------- Setup ----------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
HISTORY_FILE = "history.log"

flask_app = Flask(__name__)
flask_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
socketio = SocketIO(flask_app, cors_allowed_origins="*")

# ---------------- Backend APIs ----------------
@flask_app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    log_history("Upload", filename)
    socketio.emit("file_added", {"filename": filename})
    return "File uploaded successfully!"

@flask_app.route("/download/<filename>")
def download_file(filename):
    log_history("Download", filename)
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# ---------------- Utilities ----------------
def log_history(action, filename):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {action}: {filename}\n")

# ---------------- GUI ----------------
def start_gui():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    global root
    root = ctk.CTk()
    root.title("NETLAB - Desktop")
    root.geometry("600x700")
    
    global files_frame
    files_frame = ctk.CTkScrollableFrame(root)
    files_frame.pack(fill="both", expand=True)
    
    refresh_file_list()
    root.mainloop()

def refresh_file_list():
    for widget in files_frame.winfo_children():
        widget.destroy()
    for file in os.listdir(UPLOAD_FOLDER):
        frame = ctk.CTkFrame(files_frame, fg_color="#F0F0F0")
        frame.pack(fill="x", pady=2, padx=5)
        btn = ctk.CTkButton(frame, text=file)
        btn.pack(side="left")

# ---------------- SocketIO events ----------------
@socketio.on("connect")
def handle_connect():
    print("Mobile connected")

@socketio.on("delete_file")
def handle_delete(data):
    filename = data.get("filename")
    if filename and os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        log_history("Delete", filename)
        socketio.emit("file_deleted", {"filename": filename})
        refresh_file_list()

# ---------------- Run App ----------------
if __name__ == "__main__":
    threading.Thread(target=lambda: socketio.run(flask_app, host="0.0.0.0", port=5000), daemon=True).start()
    start_gui()
