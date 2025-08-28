from kivy.uix.screenmanager import Screen
import sqlite3

class LoginScreen(Screen):
    def login_user(self):
        uname = self.ids.username.text
        pwd = self.ids.password.text
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(uname,pwd))
        if cursor.fetchone():
            self.manager.current = "home"
        else:
            self.ids.login_label.text = "Invalid username or password!"
        conn.close()
