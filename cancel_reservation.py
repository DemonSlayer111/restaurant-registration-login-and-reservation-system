import sys
import subprocess
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from reservation_system import ReservationService


class CancelReservation(App):
    def build(self):
        self.current_user = sys.argv[1] if len(sys.argv) > 1 else ""
        self.service = ReservationService()
        self.title = "Cancel Reservation"

        layout = BoxLayout(orientation="vertical", padding=30, spacing=12)

        title_label = Label(
            text=f"Cancel Reservation - {self.current_user}",
            font_size=22,
            bold=True
        )

        info_label = Label(
            text="Press the button below to cancel your reservation.",
            font_size=16
        )

        cancel_button = Button(text="Delete Reservation", font_size=18)
        back_button = Button(text="Back", font_size=18)

        cancel_button.bind(on_press=self.cancel_reservation)
        back_button.bind(on_press=self.go_back)

        layout.add_widget(title_label)
        layout.add_widget(info_label)
        layout.add_widget(cancel_button)
        layout.add_widget(back_button)

        return layout

    def show_popup_and_return(self, title, message):
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        message_label = Label(text=message)
        ok_button = Button(text="OK")

        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(None, None),
            size=(420, 220),
            auto_dismiss=False
        )

        def close_and_return(instance):
            popup.dismiss()
            self.go_back(None)

        ok_button.bind(on_press=close_and_return)
        popup_layout.add_widget(message_label)
        popup_layout.add_widget(ok_button)
        popup.open()

    def cancel_reservation(self, instance):
        try:
            deleted = self.service.cancel_reservation(self.current_user)
        except Exception as error:
            self.show_popup_and_return("File Error", f"Could not cancel reservation.\n{error}")
            return

        if not deleted:
            self.show_popup_and_return("Cancel Reservation", "No reservation found")
            return

        self.show_popup_and_return("Cancel Reservation", "Reservation cancelled successfully")

    def go_back(self, instance):
        file_path = Path(__file__).parent / "reservation_menu.py"
        subprocess.Popen([sys.executable, str(file_path), self.current_user])
        self.stop()


if __name__ == "__main__":
    CancelReservation().run()