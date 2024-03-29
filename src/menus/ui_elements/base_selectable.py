"""
    BaseSelectable class file
"""
from blessed import Terminal
from blessed.keyboard import Keystroke

from src.app import App
from src.termutil import print_at
from .base_element import BaseElement

class BaseSelectable(BaseElement):
    """ Base Ui selectable element """

    SIDES = {
        'left':  0,
        'down':  1,
        'up':    2,
        'right': 3,
        # TAB
        'next':  4,
        'prev':  5,
    }
    """ Connectable sides of a selectable (override the values to disable it) """

    def __init__(self, width, style=None, attachments:dict=None, clear_terminal_move=True):
        super().__init__(width, style)
        self._attachments = {}
        # apply default style
        self._is_selected = False
        self._clear_terminal = clear_terminal_move

        if attachments:
            for side,element in attachments.items():
                self.connect_side(side, element)

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

    def handle_inputs(self, val: Keystroke, _terminal: Terminal):
        """ 
        Handle inputs and return the
        new selected object

        :rtype: BaseSelectable
        :returns: Return the new selected item (can be itself)
        
        """
        ret = self
        match val.name:
            case "KEY_DOWN":
                ret = self._handle_selection_input('down')
            case "KEY_UP":
                ret = self._handle_selection_input('up')
            case "KEY_LEFT":
                ret = self._handle_selection_input('left')
            case "KEY_RIGHT":
                ret = self._handle_selection_input('right')
            case "KEY_TAB":
                ret = self._handle_selection_input('next')
            case "KEY_BTAB":
                ret = self._handle_selection_input('prev')
        return ret

    def _switch_to(self, target):
        """ Switch to other thing """
        if target == self:
            return
        self.deselect()
        if self._clear_terminal:
            App.get_instance().clear()
        target.select()

    def _draw_selection_effect(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the selection effect (i.e: > Button <)"""
        offset_x = self._style.anchor_pos(self._width)
        # selection effect
        if self._is_selected:
            offset_x += self._width + self._SELECT_INDICATOR_MARGIN
            anchor = self._style.get("anchor")
            match anchor:
                case 'left':
                    print_at(terminal, \
                        pos_x-self._SELECT_INDICATOR_MARGIN, pos_y,\
                        terminal.blink(">") + terminal.normal\
                    )
                case 'center':
                    print_at(terminal, \
                        pos_x-offset_x, pos_y,\
                        terminal.blink(">") + terminal.normal\
                    )
                    print_at(terminal, \
                        pos_x+offset_x, pos_y,\
                        terminal.blink("<") + terminal.normal\
                    )
                case 'right':
                    print_at(terminal, \
                        pos_x+offset_x, pos_y,\
                        terminal.blink("<") + terminal.normal\
                    )

    def _handle_selection_input(self, side):
        if self._connected_to(side):
            ret = self._attachments.get(self.SIDES.get(side))
            self._switch_to(ret)
            return ret
        return self

    def draw(self, _terminal: Terminal, _pos_x: int, _pos_y: int):
        """ Draw the element """
        return
