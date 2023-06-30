"""
    Drop down file class
"""

import logging
from blessed import Terminal

from src.menus.ui_elements.element_style import ElementStyle
from src.menus.ui_elements.base_selectable import BaseSelectable
from src.termutil import print_at

class DropDown(BaseSelectable):
    """ Drop down """
    def __init__(self, width, options:list[tuple[str,any]]=[], button_text='', selected=0, style=None, attachments=None):
        super().__init__(width, style=ElementStyle.create_with_defaults({
            'align': 'center', 'anchor': 'center', 'background': False
        }, style), attachments=attachments)
        self._options  = options
        self._selected = selected
        self._choosing = False
        self._button_text = button_text

        self._callback = lambda *args: None
        self._callback_args = []
        self._callback_kwargs = {}
        
        if self._width < 10:
            logging.warn("Dropdown elements can't have width < 10")
            self._width = min(10, self._width)
        
    def set_on_change(self, callback: callable, *callback_args, **callback_kwargs):
        """ Set on change callback 
            :callback: the callback function, it must accept as first argument the option's name
        """
        self._callback = callback.__call__
        self._callback_args = callback_args
        self._callback_kwargs = callback_kwargs
        return self

    def set_choosing(self, value:bool):
        self._choosing = value
    
    @property
    def options(self):
        return self._options

    def draw(self, terminal: Terminal, pos_x, pos_y):
        # show selected + dropdown
        text = self._button_text
        if len(self._button_text) == 0: # show selected option
            text = self._options[self._selected][0].center(self._width-2)
        text += ' v' if self._choosing else ' >'
        aligned,_ = self._style.align(terminal, text, self._width)
        offset_x = self._style.anchor_pos(self._width)
        if self._selected:
            aligned = terminal.reverse + aligned + terminal.normal
        print_at(terminal, pos_x + offset_x, pos_y, aligned)

        # show options
        if self._choosing:
            for index,option in enumerate(self._options):
                option_txt = f"│{terminal.center(option[0], self._width-3)} │"
                if index == self._selected:
                    option_txt = terminal.reverse + option_txt + terminal.normal
                print_at(terminal, pos_x+offset_x, pos_y+index+1, option_txt)
            bottom_txt = '└' + "─"*(self._width-2) + '┘'
            print_at(terminal, pos_x+offset_x, pos_y+len(self._options)+1, bottom_txt)
    
    def handle_inputs(self, val, terminal):
        if self._choosing: 
            match val.name:
                case "KEY_ENTER" | "KEY_ESCAPE":
                    self._choosing = False
                    # update user
                    self._callback(self._options[self._selected][1], *self._callback_args, **self._callback_kwargs)
                    print(terminal.clear)
                case "KEY_DOWN":
                    self._selected = (self._selected + 1) % len(self._options)
                case "KEY_UP":
                    self._selected = (self._selected - 1)
                    if self._selected < 0: # loop
                            self._selected = len(self._options) - 1
        else:
            if val.name == "KEY_ENTER":
                self._choosing = True
            else:
                return super().handle_inputs(val, terminal)
        return self