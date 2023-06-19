import datetime
import locale

import requests
import json

from src.menus.basemenu import BaseMenu
from src.termutil import print_at, textbox_logic, Keystroke
from src.app import App

locale.setlocale(locale.LC_ALL, "")

class LoginMenu(BaseMenu):
    """ Login menu """
    username = ""
    password = ""
    selec = 0
    maxoptions = 3 #Username, Password, Confirm
    cursorPos = [0,0]

    def __init__(self):
        super().__init__("login")

    def login(self, username, password) -> tuple:
        # pretend there's an http request in here - Guigui
        # Yeah let's just pretend - Foxy

        token = "nope"

        if username != "" and password != "":
            response = requests.post("http://localhost:8080/auth/login", data = {"username":username, "password":password}, timeout=5000)
            fullResponse = json.loads(response.text)
            if (fullResponse["code"] == 200):
                return 0, fullResponse["session"]
            else:
                return 1, ""
        else:
            return 1, ""

    def draw(self, terminal) -> None:
        lang = App.get_instance().user_settings.get_locale()
        logintext = lang.get("login") 
        print_at(terminal, (terminal.width-len(logintext))*0.5, terminal.height*0.5-5, logintext)
        print_at(terminal, (terminal.width-40)*0.5, terminal.height*0.5-2, terminal.center(lang.get("username"), 40))
        print_at(terminal, (terminal.width-40)*0.5, terminal.height*0.5-1, terminal.reverse + terminal.center(self.username, 40) + terminal.normal)
        print_at(terminal, (terminal.width-40)*0.5, terminal.height*0.5+1, terminal.center(lang.get("password"), 40))
        print_at(terminal, (terminal.width-40)*0.5, terminal.height*0.5+2, terminal.reverse + terminal.center("*"*len(self.password), 40) + terminal.normal)

        print_at(terminal, (terminal.width-20)*0.5, terminal.height*0.5+4, terminal.reverse + terminal.center(lang.get("connect"), 20))

        match self.selec:
            case 0:
                print_at(terminal, (terminal.width-44)*0.5, terminal.height*0.5-1, terminal.normal + terminal.blink(">"))
            case 1:
                print_at(terminal, (terminal.width-44)*0.5, terminal.height*0.5+2, terminal.normal + terminal.blink(">"))
            case 2:
                print_at(terminal, (terminal.width-24)*0.5, terminal.height*0.5+4, terminal.normal + terminal.blink(">"))
                print_at(terminal, (terminal.width+24)*0.5, terminal.height*0.5+4, terminal.normal + terminal.blink("<"))

        dt = datetime.datetime.now()

        print_at(terminal, 1,terminal.height-2, terminal.normal + f"Il est {dt.strftime('%H:%M:%S')}, nous sommes le {dt.strftime('%A %d %B %Y')}.")


    def handle_input(self, terminal) -> None:
        val:Keystroke = super().handle_input(terminal)
        if val.name in ["KEY_UP", "KEY_DOWN"]:
            self.selec += {"KEY_UP":-1, "KEY_DOWN":1}[val.name]
            self.selec %= self.maxoptions
            print(terminal.clear)
        match self.selec:
            case 0:
                self.username, self.cursorPos[0] = textbox_logic(self.username, self.cursorPos[0], val)
            case 1:
                self.password, self.cursorPos[1] = textbox_logic(self.password, self.cursorPos[1], val)
            case 2:
                if val.name == "KEY_ENTER":
                    coderesult, newtoken = self.login(self.username, self.password)
                    if coderesult == 0:
                        app = App.get_instance()
                        app.token = newtoken
                        app.show_menu("chat")
                        app.get_menu("chat").connect(app.token)
                        print(terminal.clear)

 