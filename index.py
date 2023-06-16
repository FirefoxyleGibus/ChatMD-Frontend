from src.loginmenu import *
from src.chatmenu import *
from src.termutil import term
import src.termutil as _g

_g.menus["login"] = LoginMenu()
_g.menus["chat"] = ChatMenu()


if __name__ == "__main__":
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        while not _g.menus[_g.curmenu].turnOff:
            _g.menus[_g.curmenu].draw()
            _g.menus[_g.curmenu].handle_input()