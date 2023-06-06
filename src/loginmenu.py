from src.basemenu import BaseMenu
from src.termutil import *
import time
import locale
locale.setlocale(locale.LC_ALL, "")

class LoginMenu(BaseMenu):
    username = ""
    password = ""
    selec = 0
    maxoptions = 3 #Username, Password, Confirm
    cursorPos = [0,0]

    def login(self, username, password) -> tuple:

        # pretend there's an http request in here

        token = "nope"

        if username != "" and password != "":
            return 0, token
        else:
            return 1, ""

    def draw(self) -> None:
        logintext = "Salut!"
        print_at((term.width-len(logintext))*0.5, term.height*0.5-5, logintext)
        print_at((term.width-40)*0.5, term.height*0.5-2, term.center("Nom d'utilisateur", 40))
        print_at((term.width-40)*0.5, term.height*0.5-1, term.reverse + term.center(self.username, 40) + term.normal)
        print_at((term.width-40)*0.5, term.height*0.5+1, term.center("Mot de passe", 40))
        print_at((term.width-40)*0.5, term.height*0.5+2, term.reverse + term.center("*"*len(self.password), 40) + term.normal)

        print_at((term.width-20)*0.5, term.height*0.5+4, term.reverse + term.center("Se connecter", 20))

        match self.selec:
            case 0:
                print_at((term.width-44)*0.5, term.height*0.5-1, term.normal + term.blink(">"))
            case 1:
                print_at((term.width-44)*0.5, term.height*0.5+2, term.normal + term.blink(">"))
            case 2:
                print_at((term.width-24)*0.5, term.height*0.5+4, term.normal + term.blink(">"))
                print_at((term.width+24)*0.5, term.height*0.5+4, term.normal + term.blink("<"))

        t = time.gmtime(time.time())

        print_at(1,term.height-2, term.normal + f"Il est {time.strftime('%H:%M:%S', t)}, nous sommes le {time.strftime('%A%e %B %Y', t)}.")


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
                        global token, curmenu
                        token = newtoken

                        # - TODO: create chat interface
                        # curmenu = "chat"
                        self.turnOff = True # supprime cette ligne une fois que l'interface de chat est crée
