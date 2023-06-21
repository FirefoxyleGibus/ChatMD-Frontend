from blessed import Terminal
from blessed.keyboard import Keystroke

class BaseSelectable():
    """ Base Ui selectable element """

    SIDES = {
        'left':  0,
        'down':  1,
        'up':    2,
        'right': 3
    }
    """ Connectable sides of a selectable """

    def __init__(self, attachments=None):
        self._attachments = {}
        self._is_selected = False

        if not attachments is None:
            for side, element in enumerate(attachments):
                self.connect_side(side, element)

    def select(self) -> None:
        """ Select this element """
        self._is_selected = True

    def connect_side(self, side: str, element) -> None:
        """ Connect a button to a side """
        if side in self.SIDES:
            self._attachments[self.SIDES[side]] = element

    def handle_inputs(self, val: Keystroke) -> None:
        """ Handle inputs """
        match val:
            case "KEY_DOWN":
                self._attachments.get(self.SIDES['down'], self).select()
            case "KEY_UP":
                self._attachments.get(self.SIDES['up'], self).select()
            case "KEY_LEFT":
                self._attachments.get(self.SIDES['left'], self).select()
            case "KEY_RIGHT":
                self._attachments.get(self.SIDES['right'], self).select()
        return val

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the element """
        pass

