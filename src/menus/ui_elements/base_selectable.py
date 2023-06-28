"""
    BaseSelectable class file
"""
from blessed import Terminal
from blessed.keyboard import Keystroke

from src.menus.ui_elements.base_element import BaseElement
from src.menus.ui_elements.element_style import ElementStyle

class BaseSelectable(BaseElement):
    """ Base Ui selectable element """

    SIDES = {
        'left':  0,
        'down':  1,
        'up':    2,
        'right': 3
    }
    """ Connectable sides of a selectable (override the values to disable it) """

    def __init__(self, style=None, attachments=None, clear_terminal_move=True):
        super().__init__(style)
        self._attachments = {}
        # apply default style
        self._is_selected = False
        self._clear_terminal = clear_terminal_move

        if attachments:
            for side in attachments:
                self.connect_side(side, attachments[side])

    def select(self) -> None:
        """ Select this element """
        self._is_selected = True

    def deselect(self) -> None:
        """ Deselect this element (block user navigation to connected elements) """
        self._is_selected = False

    @property
    def is_selected(self) -> bool:
        """ Return true if this button is selected """
        return self._is_selected

    def connect_side(self, side: str, element) -> None:
        """ Connect a button to a side """
        if side in self.SIDES:
            self._attachments[self.SIDES[side]] = element

    def _connected_to(self, side) -> bool:
        """ Return if this side is connected """
        return side in self.SIDES and self.SIDES[side] in self._attachments

    def handle_inputs(self, val: Keystroke, terminal: Terminal):
        """ 
        Handle inputs and return the
        new selected object

        :rtype: BaseSelectable
        :returns: Return the new selected item (can be itself)
        
        """
        ret = self
        match val.name:
            case "KEY_DOWN" if self._connected_to('down'):
                self.deselect()
                ret = self._attachments.get(self.SIDES.get('down'))
                if self._clear_terminal:
                    print(terminal.clear)
                ret.select()
            case "KEY_UP" if self._connected_to('up'):
                self.deselect()
                ret = self._attachments.get(self.SIDES.get('up'))
                if self._clear_terminal:
                    print(terminal.clear)
                ret.select()
            case "KEY_LEFT" if self._connected_to('left'):
                self.deselect()
                ret = self._attachments.get(self.SIDES.get('left'))
                if self._clear_terminal:
                    print(terminal.clear)
                ret.select()
            case "KEY_RIGHT" if self._connected_to('right'):
                self.deselect()
                ret = self._attachments.get(self.SIDES.get('right'))
                if self._clear_terminal:
                    print(terminal.clear)
                ret.select()
        return ret

    def draw(self, _terminal: Terminal, _pos_x: int, _pos_y: int):
        """ Draw the element """
        return
