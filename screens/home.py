from kivy.uix.screenmanager import Screen
from plyer import notification
from kivymd.uix.list import OneLineListItem
import sqlite3

class HomeScreen(Screen):
    def on_enter(self):
        self.load_tasks()

    def add_task(self, title, desc):
        if title.strip() == "":
            return
        username = self.manager.get_screen("login").ids.username.text
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?",(username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO tasks (user_id,title,description) VALUES (?,?,?)",(user_id,title,desc))
        conn.commit()
        conn.close()
        self.load_tasks()
        notification.notify(title="MyApp", message=f"Task '{title}' added!", timeout=5)

    def load_tasks(self):
        self.ids.task_list.clear_widgets()
        username = self.manager.get_screen("login").ids.username.text
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?",(username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT title FROM tasks WHERE user_id=?",(user_id,))
        for row in cursor.fetchall():
            self.ids.task_list.add_widget(OneLineListItem(text=row[0]))
        conn.close()

    def go_settings(self):
        self.manager.current = "settings"

    def go_profile(self):
        self.manager.current = "profile"
        self.manager.get_screen("profile").load_profile(
            self.manager.get_screen("login").ids.username.text
        )
