from src.termutil import *

class BaseMenu():
    """ Base menu class """
    turnOff = False

    def __init__(self, name):
        self._name = name

    def get_name(self) -> str:
        """ Return the name of this menu """
        return self._name

    def draw(self, terminal) -> None:
        """ Draw the menu """
        print_at(terminal, 0, 0, self._name)

    def handle_input(self, terminal) -> any:
        """ Handle inputs """
        val = terminal.inkey(timeout=1/60)
        return val
