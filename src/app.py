from blessed import *
from blessed.keyboard import *

import asyncio

from src.bridge import Connection

class App:
    """ Main app class """

    def __init__(self):
        self.current_menu = ""
        self.menus = {}

        self.token = ""
        self.user_settings = None

        self.terminal = Terminal()
        self._is_running = True

        self.tasks = []
        self.websocket = Connection(self)

        App.instance = self

    def register_menu(self, menu):
        """ Register a menu """
        self.menus[menu.get_name()] = menu

    def show_menu(self, menu_name) -> bool:
        """ Show a menu """
        if menu_name in self.menus:
            self.current_menu = menu_name
            return True
        return False

    def get_menu(self, menu_name):
        """ Get the menu """
        return self.menus.get(menu_name)


    def run(self) -> None:
        """ Run """
        asyncio.run(self._main_loop())

    async def _main_loop(self):
        self.tasks = [
            asyncio.create_task(self.websocket.run()),
            asyncio.create_task(self._draw_screen())
        ]

    def _draw_screen(self):
        term = self.terminal
        self._is_running = True
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.clear)
            while self._is_running \
                and not self.get_menu(self.current_menu).turnOff:
                self.draw()
                self.handle_input()



    def draw(self):
        """ Show the current menu """
        if self.current_menu:
            self.get_menu(self.current_menu).draw(self.terminal)

    def handle_input(self):
        """ Handle inputs for the current menu """
        if self.current_menu:
            self.get_menu(self.current_menu).handle_input(self.terminal)
    
    def quit(self):
        """ Quit the application """
        for task in self.tasks:
            task.close()
        
        try:
            self.get_menu("chat").connection.close()
        except:
            pass
        self._is_running = False

    @staticmethod
    def get_instance():
        """ Return the app instance """
        return App.instance
