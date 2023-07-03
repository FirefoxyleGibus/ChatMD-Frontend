""" 
    Base Menu class file
"""
import logging
from blessed import Terminal

from src.termutil import print_at
from .ui_elements.base_selectable import BaseSelectable


class BaseMenu():
    """ Base menu class """
    turnOff = False

    def __init__(self, name):
        self._name = name
        self._selected = None
        logging.info("Menu <%s> was created", self._name)
    
    def start(self):
        """ Called when shown """
        return

    def get_name(self) -> str:
        """ Return the name of this menu """
        return self._name

    def focus_selectable(self, selectable: BaseSelectable):
        """ Register a selectable element """
        if not selectable is None:
            if not self._selected is None:
                self._selected.deselect()
            self._selected = selectable
            self._selected.select()

    def draw(self, terminal: Terminal) -> None:
        """ Draw the menu """
        print_at(terminal, 0, 0, self._name)

    def handle_input(self, terminal: Terminal) -> any:
        """ Handle inputs """
        val = terminal.inkey(timeout=1/60, esc_delay=0)
        if self._selected:
            self._selected = self._selected.handle_inputs(val, terminal)
        return val
