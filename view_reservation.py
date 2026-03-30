import sys
import subprocess
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from reservation_system import ReservationService


class ViewReservationApp(App):
    def build(self):
        self.current_user = sys.argv[1] if len(sys.argv) > 1 else ""
        self.service = ReservationService()
        self.title = "View Reservation"

        layout = BoxLayout(orientation="vertical", padding=30, spacing=12)

        title_label = Label(
            text=f"View Reservation - {self.current_user}",
            font_size=22,
            bold=True
        )

        self.reservation_label = Label(text="", font_size=16)

        back_button = Button(text="Back", font_size=18)
        back_button.bind(on_press=self.go_back)

        layout.add_widget(title_label)
        layout.add_widget(self.reservation_label)
        layout.add_widget(back_button)

        self.load_reservation()
        return layout

    def load_reservation(self):
        reservation = self.service.view_reservation(self.current_user)
        if reservation is None:
            self.reservation_label.text = "No reservation found"
            return

        self.reservation_label.text = (
            "Reservation Details\n\n"
            f"Number of days: {reservation.number_of_days}\n"
            f"From Date: {reservation.from_date}\n"
            f"To Date: {reservation.to_date}\n"
            f"Number of Persons: {reservation.persons}\n"
            f"Number of rooms: {reservation.rooms}"
        )

    def go_back(self, instance):
        file_path = Path(__file__).parent / "reservation_menu.py"
        subprocess.Popen([sys.executable, str(file_path), self.current_user])
        self.stop()


if __name__ == "__main__":
    ViewReservationApp().run()