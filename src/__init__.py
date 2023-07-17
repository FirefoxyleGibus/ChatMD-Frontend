"""
    ChatMD Entry
"""
import datetime
import asyncio

from .user_prefs.user_settings import UserSettings
from .app import App
from .menus import ChatMenu, LoginMenu, RegisterMenu, ExampleMenu, ProfileMenu

def main():
    """ function Entry point """
    app = App()
    app.user_settings = UserSettings()
    app.user_settings.set("last_opened", datetime.datetime.now().strftime('%H:%M:%S %A %d %B %Y'))

    app.register_menu(LoginMenu())
    app.register_menu(RegisterMenu())
    app.register_menu(ChatMenu())
    app.register_menu(ProfileMenu())
    app.register_menu(ExampleMenu())

    # Start on a specific menu
    app.show_menu("login")

    app.run()
