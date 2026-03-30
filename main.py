import sys
import subprocess
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class MainMenu(App):
    def build(self):
        self.title = "Restaurant Reservation"

        layout = BoxLayout(orientation="vertical", padding=30, spacing=15)

        welcome_label = Label(
            text="Welcome to the Restaurant Reservation System",
            font_size=22,
            bold=True
        )

        register_button = Button(
            text="Register / Signup",
            font_size=18,
            size_hint=(1, 0.2)
        )

        register_button.bind(on_press=self.open_registration)

        login_button = Button(
            text="Login",
            font_size=18,
            size_hint=(1, 0.2)
        )
        login_button.bind(on_press=self.open_login)

        exit_button = Button(
            text="Exit",
            font_size=18,
            size_hint=(1, 0.2)
        )
        exit_button.bind(on_press=self.exit_program)

        layout.add_widget(welcome_label)
        layout.add_widget(register_button)
        layout.add_widget(login_button)
        layout.add_widget(exit_button)

        return layout
    
    def open_registration(self, instance):
        file_path = Path(__file__).parent / "REGISTRATION.py"
        subprocess.Popen([sys.executable, str(file_path)])
        self.stop()

    def open_login(self, instance):
        file_path = Path(__file__).parent / "LOGIN.py"
        subprocess.Popen([sys.executable, str(file_path)])
        self.stop()

    def exit_program(self, instance):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        message = Label(text="Thank you for using our Reservation System")
        close_button = Button(text="Close", size_hint=(1, 0.4))

        popup = Popup(
            title="Exit",
            content=popup_layout,
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False
        )

        close_button.bind(on_press=lambda x: self.stop())

        popup_layout.add_widget(message)
        popup_layout.add_widget(close_button)

        popup.open()

if __name__ == "__main__":
    MainMenu().run()