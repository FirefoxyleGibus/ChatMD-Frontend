from src.termutil import *
from src.menus.ui_elements.base_selectable import BaseSelectable

class BaseMenu():
    """ Base menu class """
    turnOff = False

    def __init__(self, name):
        self._name = name
        self._selectable_elements = []

    def get_name(self) -> str:
        """ Return the name of this menu """
        return self._name
    
    def register_selectable(self, selectable: BaseSelectable):
        """ Register a selectable element """
        if not selectable is None:
            self._selectable_elements.append(selectable)

    def draw(self, terminal) -> None:
        """ Draw the menu """
        print_at(terminal, 0, 0, self._name)

    def handle_input(self, terminal) -> any:
        """ Handle inputs """
        val = terminal.inkey(timeout=1/60, esc_delay=0)
        for element in self._selectable_elements:
            element.handle_inputs(val)
        return val
