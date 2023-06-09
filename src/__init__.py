"""
    ChatMD Entry
"""
import datetime
import asyncio

from src.user_prefs.user_settings import UserSettings
from src.app import App
from src.menus import ChatMenu, LoginMenu, RegisterMenu #, ExampleMenu

def main():
    """ function Entry point """
    app = App()
    app.user_settings = UserSettings()
    app.user_settings.set("last_opened", datetime.datetime.now().strftime('%H:%M:%S %A %d %B %Y'))

    app.register_menu(LoginMenu())
    app.register_menu(RegisterMenu())
    app.register_menu(ChatMenu())
    # app.register_menu(ExampleMenu())

    # Start on a specific menu
    app.show_menu("login")

    app.run()
