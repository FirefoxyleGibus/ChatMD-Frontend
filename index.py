from src.loginmenu import *
from src.chatmenu import *
from src.termutil import *

menus:dict[str, BaseMenu] = {
    "login": LoginMenu(),
    "chat": ChatMenu()
}
curmenu = "chat"

token = ""

if __name__ == "__main__":
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        while not menus[curmenu].turnOff:
            menus[curmenu].draw()
            menus[curmenu].handle_input()