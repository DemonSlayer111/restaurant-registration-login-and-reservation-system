import sys
import subprocess
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class ReservationMenu(App):
    def build(self):
        self.current_user = sys.argv[1] if len(sys.argv) > 1 else "User"
        self.title = "Reservation Menu"

        layout = BoxLayout(orientation="vertical", padding=30, spacing=12)

        title_label = Label(
            text=f"Welcome, {self.current_user}",
            font_size=24,
            bold=True
        )

        subtitle_label = Label(
            text="Reservation Options",
            font_size=18
        )

        view_button = Button(text="View Reservation", font_size=18)
        make_button = Button(text="Make Reservation", font_size=18)
        modify_button = Button(text="Modify Reservation", font_size=18)
        cancel_button = Button(text="Cancel Reservation", font_size=18)
        logout_button = Button(text="Logout", font_size=18)

        view_button.bind(on_press=self.view_reservation)
        make_button.bind(on_press=self.make_reservation)
        modify_button.bind(on_press=self.modify_reservation)
        cancel_button.bind(on_press=self.cancel_reservation)
        logout_button.bind(on_press=self.logout)

        layout.add_widget(title_label)
        layout.add_widget(subtitle_label)
        layout.add_widget(view_button)
        layout.add_widget(make_button)
        layout.add_widget(modify_button)
        layout.add_widget(cancel_button)
        layout.add_widget(logout_button)

        return layout

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        message_label = Label(text=message)
        close_button = Button(text="Close", size_hint=(1, 0.35))

        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(None, None),
            size=(420, 220),
            auto_dismiss=False
        )

        close_button.bind(on_press=popup.dismiss)

        popup_layout.add_widget(message_label)
        popup_layout.add_widget(close_button)

        popup.open()

    def view_reservation(self, instance):
        file_path = Path(__file__).parent / "view_reservation.py"
        subprocess.Popen([sys.executable, str(file_path), self.current_user])
        self.stop()

    def make_reservation(self, instance):
        file_path = Path(__file__).parent / "make_reservation.py"
        subprocess.Popen([sys.executable, str(file_path), self.current_user])
        self.stop()

    def modify_reservation(self, instance):
        file_path = Path(__file__).parent / "modify_reservation.py"
        subprocess.Popen([sys.executable, str(file_path), self.current_user])
        self.stop()

    def cancel_reservation(self, instance):
        file_path = Path(__file__).parent / "cancel_reservation.py"
        subprocess.Popen([sys.executable, str(file_path), self.current_user])
        self.stop()
        
    def logout(self, instance):
        file_path = Path(__file__).parent / "main.py"
        subprocess.Popen([sys.executable, str(file_path)])
        self.stop()


if __name__ == "__main__":
    ReservationMenu().run()