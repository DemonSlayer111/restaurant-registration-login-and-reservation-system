import sys
import subprocess
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from reservation_system import ReservationService


class MakeReservation(App):
    def build(self):
        self.current_user = sys.argv[1] if len(sys.argv) > 1 else ""
        self.service = ReservationService()
        self.title = "Make Reservation"

        layout = BoxLayout(orientation="vertical", padding=30, spacing=10)

        title_label = Label(
            text=f"Make Reservation - {self.current_user}",
            font_size=22,
            bold=True
        )

        days_label = Label(text="Number of days:", font_size=16)
        self.days_input = TextInput(multiline=False, font_size=16)

        from_date_label = Label(text="From Date (YYYY-MM-DD):", font_size=16)
        self.from_date_input = TextInput(multiline=False, font_size=16)

        to_date_label = Label(text="To Date (YYYY-MM-DD):", font_size=16)
        self.to_date_input = TextInput(multiline=False, font_size=16)

        persons_label = Label(text="Number of Persons:", font_size=16)
        self.persons_input = TextInput(multiline=False, font_size=16)

        rooms_label = Label(text="Number of rooms:", font_size=16)
        self.rooms_input = TextInput(multiline=False, font_size=16)

        reserve_button = Button(text="Reserve", font_size=18)
        back_button = Button(text="Back", font_size=18)

        reserve_button.bind(on_press=self.save_reservation)
        back_button.bind(on_press=self.go_back)

        layout.add_widget(title_label)
        layout.add_widget(days_label)
        layout.add_widget(self.days_input)
        layout.add_widget(from_date_label)
        layout.add_widget(self.from_date_input)
        layout.add_widget(to_date_label)
        layout.add_widget(self.to_date_input)
        layout.add_widget(persons_label)
        layout.add_widget(self.persons_input)
        layout.add_widget(rooms_label)
        layout.add_widget(self.rooms_input)
        layout.add_widget(reserve_button)
        layout.add_widget(back_button)

        return layout

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        message_label = Label(text=message)
        close_button = Button(text="Close")

        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(None, None),
            size=(450, 220),
            auto_dismiss=False
        )

        close_button.bind(on_press=popup.dismiss)
        popup_layout.add_widget(message_label)
        popup_layout.add_widget(close_button)
        popup.open()

    def show_success_popup(self, message):
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        message_label = Label(text=message)
        ok_button = Button(text="OK")

        popup = Popup(
            title="Reservation Successful",
            content=popup_layout,
            size_hint=(None, None),
            size=(450, 220),
            auto_dismiss=False
        )

        def close_and_return(instance):
            popup.dismiss()
            self.go_back(None)

        ok_button.bind(on_press=close_and_return)
        popup_layout.add_widget(message_label)
        popup_layout.add_widget(ok_button)
        popup.open()

    def save_reservation(self, instance):
        try:
            self.service.make_reservation(
                self.current_user,
                self.days_input.text.strip(),
                self.from_date_input.text.strip(),
                self.to_date_input.text.strip(),
                self.persons_input.text.strip(),
                self.rooms_input.text.strip(),
            )
        except ValueError as error:
            self.show_popup("Input Error", str(error))
            return
        except Exception as error:
            self.show_popup("File Error", f"Could not save reservation.\n{error}")
            return

        self.show_success_popup("Your reservation has been saved.")

    def go_back(self, instance):
        file_path = Path(__file__).parent / "reservation_menu.py"
        subprocess.Popen([sys.executable, str(file_path), self.current_user])
        self.stop()


if __name__ == "__main__":
    MakeReservation().run()