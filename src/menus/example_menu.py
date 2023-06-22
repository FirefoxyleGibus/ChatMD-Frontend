import logging 

from src.menus.basemenu import BaseMenu
from src.menus.ui_elements import Button, TextBox, TextBoxPassword

class ExampleMenu(BaseMenu):
    """ Example menu class """

    SIZE = 20

    def __init__(self):
        super().__init__("example")
        buttons = {}
        centerbt = Button("Center", self.SIZE)
        buttons["up"]    = Button("Top", self.SIZE, attach={'down': centerbt})
        buttons["right"] = Button("Right", self.SIZE, align='right', attach={'left': centerbt })
        buttons["left"]  = Button("Left", self.SIZE, align='left', attach={'right': centerbt })
        buttons["down"]  = Button("Bottom", self.SIZE, attach={'up': centerbt })

        self._textbox = TextBox(60, "Type text...", ">>> ", False, 'center', 'left', attach={
            'up': buttons['down'],
        })
        buttons['down'].connect_side('down', self._textbox)
        self._pass = TextBoxPassword(60, attach={'up': self._textbox})
        self._textbox.connect_side('down', self._pass)

        for side,button in buttons.items():
            centerbt.connect_side(side, button)

        buttons["center"] = centerbt
        self._buttons = buttons
        self.focus_selectable(centerbt)

    def _log(self, message):
        """ Log something """
        logging.debug("DebugMenu says: %s", message)

    def draw(self, terminal):
        super().draw(terminal)

        center_x, center_y = terminal.width//2, terminal.height//2
        offset_x = self.SIZE * 2 - 5

        self._buttons["center"].draw(terminal, center_x, center_y)
        self._buttons["up"].draw(terminal, center_x, center_y-2)
        self._buttons["down"].draw(terminal, center_x, center_y+2)
        self._buttons["left"].draw(terminal, center_x - offset_x, center_y)
        self._buttons["right"].draw(terminal, center_x + offset_x, center_y)
        self._textbox.draw(terminal, center_x, center_y+6)
        self._pass.draw(terminal, center_x, center_y+8)