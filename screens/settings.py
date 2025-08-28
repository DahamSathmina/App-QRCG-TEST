from kivy.uix.screenmanager import Screen
from kivy.app import App

class SettingsScreen(Screen):
    def toggle_theme(self):
        App.get_running_app().toggle_theme()

    def go_home(self):
        self.manager.current = "home"
