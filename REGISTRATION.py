import sys
import subprocess
from pathlib import Path

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import os

LoginInfo = "users"

if not os.path.exists(LoginInfo):
    os.makedirs(LoginInfo)
#declares file names that get created during registration proccess
def user_file(lastName):
        return os.path.join(LoginInfo, f"{lastName}.txt")

class registrationApp(App):

    #creates window
    def build(self):
        #title for window
        self.title = "Register"
        #set size and spacing of textboxes inside
        layout = BoxLayout(orientation = 'vertical', padding = 30, spacing = 10)

        #header
        headLabel = Label(text = "Restaurant Account Registration", font_size = 18, bold = True, height = 40)

        #Email
        emailLabel = Label(text = "Enter Email: ", font_size = 12)
        self.emailInput = TextInput(multiline = False, font_size = 12)
        #first name and last name
        firstNameLabel = Label(text = "Enter First name: ", font_size = 12)
        self.firstNameInput = TextInput(multiline = False, font_size = 12)
        #last name
        lastNameLabel = Label(text = "Enter Last Name: ", font_size = 12)
        self.lastNameInput = TextInput(multiline = False, font_size = 12)
        #password
        passwordLabel = Label(text = "Enter Password: ", font_size = 12)
        self.passwordInput = TextInput(multiline = False, font_size = 12)
        #birthdate
        birthdateLabel = Label(text = "Enter Birthdate: ", font_size = 12)
        self.birthdateInput = TextInput(multiline = False, font_size = 12)

        #buttons
        submitButton = Button(text = 'submit', font_size = 12, on_press = self.register)
        cancelButton = Button(text = 'cancel', font_size = 12, on_press=self.go_back)

        #add labels
        layout.add_widget(headLabel)
        layout.add_widget(emailLabel)
        layout.add_widget(self.emailInput)
        layout.add_widget(firstNameLabel)
        layout.add_widget(self.firstNameInput)
        layout.add_widget(lastNameLabel)
        layout.add_widget(self.lastNameInput)
        layout.add_widget(passwordLabel)
        layout.add_widget(self.passwordInput)
        layout.add_widget(birthdateLabel)
        layout.add_widget(self.birthdateInput)
        layout.add_widget(submitButton)
        layout.add_widget(cancelButton)

        return layout

    def register(self, instance):
        #define variables
        email = self.emailInput.text
        firstname = self.firstNameInput.text
        lastname = self.lastNameInput.text
        password = self.passwordInput.text
        birthdate = self.birthdateInput.text
        path = user_file(lastname)
        success = False
        #checks for invalid input
        while success == False:
            try:
                if int(email) or int(firstname) or int(lastname):
                    message = "invalid input"   
            except ValueError:        
                #check if boxes are filled
                if email.strip() == '' or firstname.strip() == '' or lastname.strip() == '' or password.strip() == '' or birthdate.strip() == '':
                    message = "please fill on all the boxes"
                else:
                    #writes files based on registration data
                    with open(path, 'w') as file:
                        file.write('{}\n'.format(email,))#email
                        file.write('{}\n'.format(password))#password
                        file.write('{}\n'.format(firstname))#firstname
                        file.write('{}\n'.format(lastname))#lastname
                        file.write('{}\n'.format(birthdate))#birthdate
                    message = "registration completed! \nName: {} {}\nEmail: {}".format(firstname, lastname, email)
                    success = True 
            break
        #post registration popup(can be an error statement) 
        #set popup window
        popup = Popup(title = "registration", content = Label(text = message), size_hint = (None, None), size = (400, 200))   
        popup.open()
        if success == True:
           self.go_back()

    def go_back(self, instance):
        file_path = Path(__file__).parent / "main.py"
        subprocess.Popen([sys.executable, str(file_path)])
        self.stop()
        
#run kivy
if __name__=='__main__':
    registrationApp().run()