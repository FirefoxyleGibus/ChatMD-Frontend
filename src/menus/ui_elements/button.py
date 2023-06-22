from blessed import Terminal
from blessed.keyboard import Keystroke

from src.menus.ui_elements.base_selectable import BaseSelectable
from src.menus.ui_elements.text_style import TextStyle
from src.termutil import print_at

class Button(BaseSelectable):
    """ Button """

    _SELECT_INDICATOR_MARGIN: int = 4
    """ Margin from the button to the blinky > button_text < """

    def __init__(self, text: str, width: int, anchor='center', align:str='center', attach:dict=None):
        super().__init__(attachments=attach)
        self._text   = text
        self._width  = width
        self._anchor = anchor
        self._align  = align
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
    
    def set_text(self, text: str):
        """ Set text of this button """
        if isinstance(text, str):
            self._text = text

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the button """
        # button background + text
        aligned_text,_ = TextStyle.align(terminal, self._align, self._text, self._width)
        text = terminal.reverse + aligned_text + terminal.normal
        offset_x = TextStyle.anchor_pos(self._anchor, self._width)
        print_at(terminal, pos_x + offset_x, pos_y, text)

        # selection effect
        if self._is_selected:
            offset_x += self._width + self._SELECT_INDICATOR_MARGIN
            if self._align in ('left', 'center'):
                print_at(terminal, \
                    pos_x-offset_x, pos_y,\
                    terminal.blink(">") + terminal.normal\
                )
            if self._align in ('right', 'center'):
                print_at(terminal, \
                    pos_x+offset_x, pos_y,\
                    terminal.blink("<") + terminal.normal\
                )
