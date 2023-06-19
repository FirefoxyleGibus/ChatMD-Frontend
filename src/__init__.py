from src.user_prefs.user_settings import UserSettings
from src.app import App

from src.menus.chatmenu import ChatMenu
from src.menus.loginmenu import LoginMenu

import datetime

def main():
    app = App()
    app.user_settings = UserSettings()
    app.user_settings.set("last_opened", datetime.datetime.now().strftime('%H:%M:%S %A %d %B %Y'))

    app.register_menu(LoginMenu())
    app.register_menu(ChatMenu())

    # Start on login menu
    app.show_menu("login")

    app.run()
