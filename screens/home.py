from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDIconButton
from plyer import notification
import sqlite3

class HomeScreen(Screen):
    def on_enter(self):
        self.load_tasks()

    # Add a new task
    def add_task(self, title, desc):
        if title.strip() == "":
            return
        username = self.manager.get_screen("login").ids.username.text
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?",(username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO tasks (user_id,title,description) VALUES (?,?,?)",
                       (user_id,title,desc))
        conn.commit()
        conn.close()
        self.load_tasks()
        notification.notify(title="MyApp", message=f"Task '{title}' added!", timeout=5)

    # Load all tasks for the logged-in user
    def load_tasks(self):
        self.ids.task_list.clear_widgets()
        username = self.manager.get_screen("login").ids.username.text
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?",(username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT id,title,completed FROM tasks WHERE user_id=?",(user_id,))
        for t in cursor.fetchall():
            task_item = self.create_task_item(t)
            if t[2] == 1:
                task_item.text = f"✔️ {t[1]}"
            self.ids.task_list.add_widget(task_item)
        conn.close()

    # Create a task item widget with delete button
    def create_task_item(self, task):
        task_item = OneLineListItem(text=task[1])
        delete_btn = MDIconButton(icon="delete", on_release=lambda x, t_id=task[0]: self.delete_task(t_id))
        task_item.add_widget(delete_btn)
        return task_item

    # Delete a task by ID
    def delete_task(self, task_id):
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?",(task_id,))
        conn.commit()
        conn.close()
        self.load_tasks()
        notification.notify(title="MyApp", message="Task deleted!", timeout=5)

    # Navigate to settings screen
    def go_settings(self):
        self.manager.current = "settings"

    # Navigate to profile screen
    def go_profile(self):
        self.manager.current = "profile"
