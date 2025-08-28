from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.home import HomeScreen
from screens.settings import SettingsScreen
from screens.profile import ProfileScreen
import sqlite3
import os

# Create data directory and database if not exist
if not os.path.exists("data"):
    os.makedirs("data")

conn = sqlite3.connect("data/app_data.db")
cursor = conn.cursor()

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT,
    avatar TEXT
)
''')

# Default user
cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username,password) VALUES (?,?)",("admin","admin"))

# Settings table
cursor.execute('''
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    theme TEXT
)
''')
cursor.execute("SELECT * FROM settings")
if not cursor.fetchone():
    cursor.execute("INSERT INTO settings (theme) VALUES ('Light')")

# Tasks table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    description TEXT,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')
conn.commit()
conn.close()

# Screen Manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name="login"))
sm.add_widget(RegisterScreen(name="register"))
sm.add_widget(HomeScreen(name="home"))
sm.add_widget(SettingsScreen(name="settings"))
sm.add_widget(ProfileScreen(name="profile"))

class MyApp(MDApp):
    def build(self):
        self.load_theme_from_db()
        return sm

    def load_theme_from_db(self):
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT theme FROM settings LIMIT 1")
        theme = cursor.fetchone()[0]
        self.theme_cls.theme_style = theme
        conn.close()

    def toggle_theme(self):
        new_theme = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.theme_cls.theme_style = new_theme
        conn = sqlite3.connect("data/app_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET theme=? WHERE id=1",(new_theme,))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    MyApp().run()
