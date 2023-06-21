from blessed import *
from blessed.keyboard import *

import asyncio
from dotenv import load_dotenv

from src.bridge import Connection

class App:
    """ Main app class """

    def __init__(self):
        load_dotenv()

        self.current_menu = ""
        self.menus = {}

        self.token = ""
        self.user_settings = None

        self.terminal = Terminal()
        self._is_running = True

        self.loop = None
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


    def run(self):
        """ Run """
        print("Application starting")
        self.loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(self._draw_screen())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Closing Loop")
            self.loop.close()
        print("Application ended")

    async def _draw_screen(self):
        term = self.terminal
        self._is_running = True
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.clear)
            while self._is_running \
                and not self.get_menu(self.current_menu).turnOff:
                await asyncio.sleep(.01)
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
        self._is_running = False
        try:
            self.websocket.close()
        except:
            pass

        if self.loop:
            self.loop.stop()

    @staticmethod
    def get_instance():
        """ Return the app instance """
        return App.instance

    @staticmethod
    def get_locale():
        """ Return the locale of the app instance """
        return App.get_instance().user_settings.get_locale()
