from src.loginmenu import *
from src.chatmenu import *
from src.termutil import term
import src.termutil as _g
from src.user_prefs.user_settings import UserSettings

def main():
    _g.user_settings = UserSettings()

    _g.user_settings.set("login_times", _g.user_settings.get("login_times", 0)+1)

    _g.menus["login"] = LoginMenu()
    _g.menus["chat"] = ChatMenu()

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        while not _g.menus[_g.curmenu].turnOff:
            _g.menus[_g.curmenu].draw()
            _g.menus[_g.curmenu].handle_input()
