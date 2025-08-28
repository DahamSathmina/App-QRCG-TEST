from kivy.uix.screenmanager import Screen
import sqlite3

class ProfileScreen(Screen):
    def load_profile(self, username):
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT email, avatar FROM users WHERE username=?",(username,))
        result = cursor.fetchone()
        if result:
            self.ids.email.text = result[0] if result[0] else ""
            self.ids.avatar.source = result[1] if result[1] else "assets/default_avatar.png"
        conn.close()

    def update_profile(self, email):
        username = self.manager.get_screen("login").ids.username.text
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email=? WHERE username=?",(email,username))
        conn.commit()
        conn.close()
        self.ids.status.text = "Profile updated!"
