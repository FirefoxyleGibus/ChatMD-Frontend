from src.basemenu import BaseMenu
from src.termutil import term, print_at, textbox_logic, Keystroke
import src.termutil as _g
import datetime
import locale
import requests
import json
locale.setlocale(locale.LC_ALL, "")

class LoginMenu(BaseMenu):
    username = ""
    password = ""
    selec = 0
    maxoptions = 3 #Username, Password, Confirm
    cursorPos = [0,0]

    def login(self, username, password) -> tuple:
        # pretend there's an http request in here - Guigui
        # Yeah let's just pretend - Foxy

        token = "nope"

        if username != "" and password != "":
            response = requests.post("http://localhost:8080/auth/login", data = {"username":username, "password":password})
            fullResponse = json.loads(response.text)
            if (fullResponse["code"] == 200):
                return 0, fullResponse["session"]
            else:
                return 1, ""
        else:
            return 1, ""

    def draw(self) -> None:
        locale = _g.user_settings.get_locale()
        logintext = locale.get("login") 
        print_at((term.width-len(logintext))*0.5, term.height*0.5-5, logintext)
        print_at((term.width-40)*0.5, term.height*0.5-2, term.center(locale.get("username"), 40))
        print_at((term.width-40)*0.5, term.height*0.5-1, term.reverse + term.center(self.username, 40) + term.normal)
        print_at((term.width-40)*0.5, term.height*0.5+1, term.center(locale.get("password"), 40))
        print_at((term.width-40)*0.5, term.height*0.5+2, term.reverse + term.center("*"*len(self.password), 40) + term.normal)

        print_at((term.width-20)*0.5, term.height*0.5+4, term.reverse + term.center(locale.get("connect"), 20))

        match self.selec:
            case 0:
                print_at((term.width-44)*0.5, term.height*0.5-1, term.normal + term.blink(">"))
            case 1:
                print_at((term.width-44)*0.5, term.height*0.5+2, term.normal + term.blink(">"))
            case 2:
                print_at((term.width-24)*0.5, term.height*0.5+4, term.normal + term.blink(">"))
                print_at((term.width+24)*0.5, term.height*0.5+4, term.normal + term.blink("<"))

        dt = datetime.datetime.now()

        print_at(1,term.height-2, term.normal + f"Il est {dt.strftime('%H:%M:%S')}, nous sommes le {dt.strftime('%A %d %B %Y')}.")


    def handle_input(self) -> None:
        val:Keystroke = super().handle_input()
        if val.name in ["KEY_UP", "KEY_DOWN"]:
            self.selec += {"KEY_UP":-1, "KEY_DOWN":1}[val.name]
            self.selec %= self.maxoptions
            print(term.clear)
        match self.selec:
            case 0:
                self.username, self.cursorPos[0] = textbox_logic(self.username, self.cursorPos[0], val)
            case 1:
                self.password, self.cursorPos[1] = textbox_logic(self.password, self.cursorPos[1], val)
            case 2:
                if val.name == "KEY_ENTER":
                    coderesult, newtoken = self.login(self.username, self.password)
                    if coderesult == 0:
                        _g.token = newtoken
                        _g.curmenu = "chat"
                        _g.menus[_g.curmenu].connect(_g.token)
                        print(term.clear)
