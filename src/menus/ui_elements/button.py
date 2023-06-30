"""
    Button class file
"""
from blessed import Terminal
from blessed.keyboard import Keystroke

from src.menus.ui_elements.base_selectable import BaseSelectable
from src.menus.ui_elements.element_style import ElementStyle
from src.termutil import print_at

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

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the button """
        # button background + text
        aligned_text,_ = self._style.align(terminal, self._text, self._width)
        text = self._style.background(terminal) + aligned_text + terminal.normal
        offset_x = self._style.anchor_pos(self._width)
        print_at(terminal, pos_x + offset_x, pos_y, text)

        self._draw_selection_effect(terminal, pos_x, pos_y)
