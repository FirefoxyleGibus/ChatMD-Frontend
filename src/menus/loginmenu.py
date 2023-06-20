import datetime

import json
import requests

from src.menus.basemenu import BaseMenu
from src.termutil import print_at, textbox_logic, Keystroke
from src.app import App
from src.menus.loginexception import LoginException

class LoginMenu(BaseMenu):
    """ Login menu """
    username = ""
    password = ""
    selec = 0
    maxoptions = 4 #Username, Password, Confirm, Quit
    cursorPos = [0,0]

    def __init__(self):
        super().__init__("login")
        self.status_message = ""

    def login(self, username, password) -> str:
        """ Log in with a username and a password """
        if username.rstrip() != "" and password.rstrip() != "":
            try:
                response = requests.post("http://localhost:8080/auth/login", data = {"username":username, "password":password}, timeout=5.0)
                full_response = json.loads(response.text)
                match full_response["code"]:
                    case 200:
                        return full_response["data"]["session"]
                    case 404:
                        raise LoginException("not_found")
            except json.JSONDecodeError:
                raise LoginException("connection_fail")
            except requests.exceptions.Timeout:
                raise LoginException("timeout")
            except requests.exceptions.TooManyRedirects:
                raise LoginException("connection_fail")
            except requests.exceptions.RequestException:
                raise LoginException("connection_fail")
        raise LoginException("missing_credentials")

    def register(self, username, password) -> tuple:
        """ Register a new user """
        if username != "" and password != "":
            response = requests.post("http://localhost:8080/auth/register", data={"username": username, "password": password}, timeout=5.0)
            full_response = json.loads(response.text)
            if (full_response["code"] == 200):
                return 0, full_response["data"]["session"]
            return 1, "token"
        return 1, ""

    def draw(self, terminal) -> None:
        lang = App.get_instance().user_settings.get_locale()
        logintext = lang.get("login") 
        print_at(terminal, (terminal.width-len(logintext))*0.5, terminal.height*0.5-5, logintext)
        print_at(terminal, (terminal.width-len(self.status_message))*0.5, terminal.height*0.5-4, terminal.red(self.status_message))
        print_at(terminal, (terminal.width-40)*0.5, terminal.height*0.5-2, terminal.center(lang.get("username"), 40))
        print_at(terminal, (terminal.width-40)*0.5, terminal.height*0.5-1, terminal.reverse + terminal.center(self.username, 40) + terminal.normal)
        print_at(terminal, (terminal.width-40)*0.5, terminal.height*0.5+1, terminal.center(lang.get("password"), 40))
        print_at(terminal, (terminal.width-40)*0.5, terminal.height*0.5+2, terminal.reverse + terminal.center("*"*len(self.password), 40) + terminal.normal)

        print_at(terminal, (terminal.width-20)*0.5, terminal.height*0.5+4, terminal.reverse + terminal.center(lang.get("connect"), 20))

        print_at(terminal, (terminal.width-20)*0.5, terminal.height*0.5+6, terminal.reverse + terminal.center(lang.get("quit"), 20))

        match self.selec:
            case 0:
                print_at(terminal, (terminal.width-44)*0.5, terminal.height*0.5-1, terminal.normal + terminal.blink(">"))
            case 1:
                print_at(terminal, (terminal.width-44)*0.5, terminal.height*0.5+2, terminal.normal + terminal.blink(">"))
            case 2:
                print_at(terminal, (terminal.width-24)*0.5, terminal.height*0.5+4, terminal.normal + terminal.blink(">"))
                print_at(terminal, (terminal.width+24)*0.5, terminal.height*0.5+4, terminal.normal + terminal.blink("<"))
            case 3:
                print_at(terminal, (terminal.width-24)*0.5, terminal.height*0.5+6, terminal.normal + terminal.blink(">"))
                print_at(terminal, (terminal.width+24)*0.5, terminal.height*0.5+6, terminal.normal + terminal.blink("<"))
        date = datetime.datetime.now()

        date_message = lang.get('date_status').format(time=date.strftime('%H:%M:%S'), date=date.strftime('%A %d %B %Y'))
        print_at(terminal, 1,terminal.height-2, terminal.normal + date_message)


    def handle_input(self, terminal) -> None:
        val:Keystroke = super().handle_input(terminal)
        lang = App.get_instance().user_settings.get_locale()
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
                    try:
                        newtoken = self.login(self.username, self.password)
                        print(terminal.clear)
                        self.status_message = ""
                        app = App.get_instance()
                        app.token = newtoken
                        app.show_menu("chat")
                        app.get_menu("chat").name = self.username
                        app.get_menu("chat").connect(app.token)
                    except LoginException as err:
                        print(terminal.clear)
                        self.status_message = lang.get(err.get_failure())

            case 3:
                if val.name == "KEY_ENTER":
                    App.get_instance().quit()

