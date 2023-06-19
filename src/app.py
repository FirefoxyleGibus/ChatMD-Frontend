from blessed import *
from blessed.keyboard import *

class App:
    """ Main app class """

    def __init__(self):
        self.current_menu = ""
        self.menus = {}

        self.token = ""
        self.user_settings = None

        self.terminal = Terminal()

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
        term = self.terminal
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.clear)
            while not self.get_menu(self.current_menu).turnOff:
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

    @staticmethod
    def get_instance():
        """ Return the app instance """
        return App.instance