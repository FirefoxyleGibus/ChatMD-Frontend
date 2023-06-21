import logging
from blessed import Terminal
from blessed.keyboard import Keystroke

from src.menus.ui_elements.base_selectable import BaseSelectable
from src.app import App
from src.termutil import print_at

class Button(BaseSelectable):
    """ Button """

    _SELECT_INDICATOR_MARGIN: int = 4
    """ Margin from the button to the blinky > button_text < """

    def __init__(self, text: str, width: int, alignement:str='center', attachments:dict=None):
        super().__init__(attachments=attachments)
        self._text = text
        self._width = width
        self._align = alignement
        # callback
        self._callback = lambda *args: None
        self._callback_args = []
        self._callback_kwargs = {}

    def set_on_click(self, callback: callable, *args, **kwargs):
        """ Set the callbcak on click """
        self._callback = callback.__call__
        self._callback_args = args
        self._callback_kwargs = kwargs
        return self

    def handle_inputs(self, val: Keystroke, terminal: Terminal):
        ret = super().handle_inputs(val, terminal)
        if val.name == "KEY_ENTER":
            self._callback(*self._callback_args, **self._callback_kwargs)
        return ret

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the button """
        lang = App.get_locale()
        match self._align:
            case "center":
                text = terminal.reverse + terminal.center(lang.get(self._text), self._width)
                print_at(terminal, pos_x - self._width // 2, pos_y, text + terminal.normal)

                if self._is_selected:
                    offset_x = self._width // 2 + self._SELECT_INDICATOR_MARGIN
                    print_at(terminal, pos_x-offset_x, pos_y, terminal.blink(">") + terminal.normal)
                    print_at(terminal, pos_x+offset_x, pos_y, terminal.blink("<") + terminal.normal)
            case 'left':
                text = terminal.reverse + terminal.ljust(lang.get(self._text), self._width)
                print_at(terminal, pos_x, pos_y, text + terminal.normal)
                if self._is_selected:
                    print_at(terminal, \
                        pos_x-self._SELECT_INDICATOR_MARGIN, pos_y,\
                        terminal.blink(">") + terminal.normal\
                    )
            case 'right':
                text = terminal.reverse + terminal.rjust(lang.get(self._text), self._width)
                # adding +1 to have the same spaces for left and right alignemnt
                print_at(terminal, pos_x - self._width+1, pos_y, text + terminal.normal)
                if self._is_selected:
                    offset_x = self._SELECT_INDICATOR_MARGIN
                    print_at(terminal, \
                        pos_x+offset_x, pos_y,\
                        terminal.blink("<") + terminal.normal\
                    )
