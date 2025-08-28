from kivy.uix.screenmanager import Screen
import sqlite3

class RegisterScreen(Screen):
    def register_user(self, username, password):
        if username == "" or password == "":
            self.ids.register_label.text = "Fields cannot be empty!"
            return
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?",(username,))
        if cursor.fetchone():
            self.ids.register_label.text = "Username already exists!"
        else:
            cursor.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
            conn.commit()
            self.ids.register_label.text = "Registration successful!"
        conn.close()
