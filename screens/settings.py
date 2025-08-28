from kivy.uix.screenmanager import Screen
from main import MyApp

class SettingsScreen(Screen):
    def toggle_theme(self):
        MyApp.get_running_app().toggle_theme()
