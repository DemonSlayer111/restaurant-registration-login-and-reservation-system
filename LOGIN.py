import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from pathlib import Path
import os
LoginInfo = "users"

if not os.path.exists(LoginInfo):
    os.makedirs(LoginInfo)
#declares file names that will be checked
def user_file(lastName):
        return os.path.join(LoginInfo, f"{lastName}.txt")

class login(App):
    #create window
    def build(self):
        self.title = "Login"
        #set size and spacing of textboxes inside
        layout = BoxLayout(orientation = 'vertical', padding = 30, spacing = 10)

        #header
        headLabel = Label(text = "account login", font_size = 26, bold = True, height = 40)

        #Email
        emailLabel = Label(text = "Enter Email: ", font_size = 18)
        self.emailInput = TextInput(multiline = False, font_size = 18)
        #password
        passwordLabel = Label(text = "Enter Password: ", font_size = 18)
        self.passwordInput = TextInput(multiline = False, font_size = 18)
        #lastname(for file recognition)
        LastNameLabel = Label(text = "Enter Last Name: ", font_size = 18)
        self.LastNameInput = TextInput(multiline = False, font_size = 18)

        #buttons
        LoginButton = Button(text = 'Login', font_size = 18, on_press = self.login)
        cancelButton = Button(text = 'cancel', font_size = 18)#attach function to return to main menu

        #add labels and buttons
        layout.add_widget(headLabel)
        layout.add_widget(emailLabel)
        layout.add_widget(self.emailInput)
        layout.add_widget(passwordLabel)
        layout.add_widget(self.passwordInput)
        layout.add_widget(LastNameLabel)
        layout.add_widget(self.LastNameInput)
        layout.add_widget(LoginButton)
        layout.add_widget(cancelButton)

        return layout

    def TryAgainpopup(self):
        #build popup
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        #popup title
        layout.add_widget(Label(text="Incorrect password or email"))
        #buttons
        TryAgain = Button(text="try again")
        close_btn = Button(text="Close")
        #button features
        TryAgain.bind(on_release=lambda x: popup.dismiss())
        close_btn.bind(on_release=lambda x: popup.dismiss())#replace with a return to main menu
        #add buttons
        layout.add_widget(TryAgain)
        layout.add_widget(close_btn)
        #convert layout to popup
        popup = Popup(title="Options", content=layout, size_hint=(0.6, 0.4), auto_dismiss=False)

        popup.open()

    def login(self,instance):#instance to avoid error
        #sets popup 
        popup = Popup(title = "login", content = Label(text = "logging in..."), size_hint = (None, None), size = (400, 200))
        #convert user input to usable vairables
        email = self.emailInput.text
        password = self.passwordInput.text
        LastName = self.LastNameInput.text
        #to read file designated by last name input
        path = user_file(LastName)
        #to catch error incase incorrect last name or user has not gone through registration proccess
        if not os.path.exists(path):
            print("User does not exist.")
            return False
        #read specified file and extract email & password
        with open(path, "r") as f:
            stored_email = f.readline().strip()
            stored_password = f.readline().strip()
        #login proccess
        if email == stored_email and password == stored_password:
             #print("success")
             popup.open()
             #enter code that sends to reservation menu
        else:
             self.TryAgainpopup()
#run kivy    
if __name__=='__main__':
    login().run()


