"""
    Button class file
"""
from blessed import Terminal
from blessed.keyboard import Keystroke

from src.termutil import print_at
from .callback import Callback
from .base_selectable import BaseSelectable
from .element_style import ElementStyle

class Button(BaseSelectable):
    """ Button """

    _SELECT_INDICATOR_MARGIN: int = 4
    """ Margin from the button to the blinky > button_text < """

    def __init__(self, text: str, width: int, style:dict=None, attach:dict=None):
        super().__init__(width, style=ElementStyle.create_with_defaults({
            'align': 'center', 
            'anchor': 'center', 
            'background': True
        }, style), attachments=attach)
        self._text   = text
        self._callback = Callback()

    def set_on_click(self, callback: callable, *args, **kwargs):
        """ Set the callback on click """
        self._callback.set_func(callback, *args, **kwargs)
        return self

    def handle_inputs(self, val: Keystroke, terminal: Terminal):
        ret = super().handle_inputs(val, terminal)
        if val.name == "KEY_ENTER":
            self._callback.call()
        return ret

    def set_text(self, text: str):
        """ Set text of this button """
        if isinstance(text, str):
            self._text = text

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the button """
        # button background + text
        aligned_text,_ = self._style.align(terminal, self._text, self._width)
        text = self._style.background(terminal) + aligned_text + terminal.normal
        offset_x = self._style.anchor_pos(self._width)
        print_at(terminal, pos_x + offset_x, pos_y, text)

        self._draw_selection_effect(terminal, pos_x, pos_y)
