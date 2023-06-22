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
    """ Connectable sides of a selectable (override the values to disable it) """

    def __init__(self, attachments=None):
        self._attachments = {}
        self._is_selected = False

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

    def handle_inputs(self, val: Keystroke, terminal: Terminal):
        """ 
        Handle inputs and return the
        new selected object

        :rtype: BaseSelectable
        :returns: Return the new selected item (can be itself)
        
        """
        ret = self
        match val.name:
            case "KEY_DOWN":
                self.deselect()
                ret = self._attachments.get(self.SIDES.get('down', len(self.SIDES)), self)
                ret.select()
                print(terminal.clear)
            case "KEY_UP":
                self.deselect()
                ret = self._attachments.get(self.SIDES.get('up', len(self.SIDES)), self)
                ret.select()
                print(terminal.clear)
            case "KEY_LEFT":
                self.deselect()
                ret = self._attachments.get(self.SIDES.get('left', len(self.SIDES)), self)
                ret.select()
                print(terminal.clear)
            case "KEY_RIGHT":
                self.deselect()
                ret = self._attachments.get(self.SIDES.get('right', len(self.SIDES)), self)
                ret.select()
                print(terminal.clear)
        return ret

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the element """
        pass
