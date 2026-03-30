# KIVY

Kivy is a window creation and editing tool

## Installation

open a new terminal, and make sure that you are using python ver 3.10.11 or earlier version, as downloading on later versions will cause errors

```bash
pip install kivy
```

## Usage

```python
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# sets window alignment, padding is distance between window wall and widgets, and spacing is distance between widgets
layout = BoxLayout(orientation = 'vertical', padding = 30, spacing = 10)

# sets a label (a body of text)
headLabel = Label(text = "account login", font_size = 26, bold = True, height = 40)

# sets a text box
self.emailInput = TextInput(multiline = False, font_size = 18)

#sets a button to be interacted with
self.passwordInput = TextInput(multiline = False, font_size = 18)

#adds widget to window
layout.add_widget(headLabel)

#adds function to buttons
TryAgain.bind(on_release=lambda x: popup.dismiss())

#sets a popup after a button press
popup = Popup(title = "login", content = Label(text = "logging in..."), size_hint = (None, None), size = (400, 200))
```

## Contributing

Earl Gabriel Tagapolot = registration and login page

Anri Zaimi = main menu, reservation menu, and reservation
