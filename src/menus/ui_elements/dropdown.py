"""
    Drop down file class
"""

import logging
from blessed import Terminal

from src.termutil import print_at
from .callback import Callback
from .element_style import ElementStyle
from .base_selectable import BaseSelectable

class DropDown(BaseSelectable):
    """ Drop down """

    _SELECT_INDICATOR_MARGIN = 2

    def __init__(self, width, options:list[tuple[str,any]]=None, \
                 button_text='', selected=0, style=None, attachments=None):
        super().__init__(width, style=ElementStyle.create_with_defaults({
            'align': 'center', 'anchor': 'center', 'background': False
        }, style), attachments=attachments)
        self._options  = options if options else []
        self._opt_select = selected
        self._previous_choice = selected
        self._choosing = False
        self._button_text = button_text

        self._callback = Callback(default=lambda *args,**kwargs: self)

        if self._width < 10:
            logging.exception("Dropdown elements can't have width < 10")
            self._width = min(10, self._width)

    def set_on_change(self, callback: callable, *args, **kwargs):
        """ Set on change callback 
            :callback: the callback function, it must accept as first argument the option's name
            and MUST return the element to focus next (can be self) 
        """
        self._callback.set_func(callback, *args, **kwargs)
        return self

    def _on_change(self, new_value):
        return self._callback.call(new_value)

    def set_choosing(self, value:bool, starting_option=None):
        """ Set choosing state of this dropdown """
        self._choosing = value
        if not starting_option is None:
            self._opt_select = min(len(self._options)-1, max(0, starting_option))


    def set_options(self, options):
        """ Set options list 
            :options: list of tuple[name, value]
        """
        self._options = options

    @property
    def options(self):
        """ Options in the dropdown
            :rtype: list[tuple(value_text, value)]
        """
        return self._options

    @property
    def render_height(self):
        """ Get final output render height """
        return len(self._options) + 2

    def draw(self, terminal: Terminal, pos_x, pos_y):
        # Show dropdown title/value
        text = self._button_text
        if len(self._button_text) == 0: # show selected option
            text = self._options[self._opt_select][0]
        text = text.center(self._width-3)
        text += ' v' if self._choosing else ' >'

        aligned,_ = self._style.align(terminal, text, self._width)
        offset_x = self._style.anchor_pos(self._width)
        if self._opt_select or self._opt_select == 0:
            aligned = ElementStyle.add_background(terminal, aligned)
        print_at(terminal, pos_x + offset_x, pos_y, aligned)

        # show options
        if self._choosing:
            # Separation box
            separation_txt = terminal.normal + '┌' + "─"*(self._width-2) + '┐'
            print_at(terminal, pos_x + offset_x, pos_y+1, separation_txt)

            # Options list
            off_y = 2
            for index,option in enumerate(self._options):
                option_txt = f"│ {terminal.center(option[0], self._width-4)} │"
                if index == self._opt_select:
                    option_txt = ElementStyle.add_background(terminal, option_txt)
                print_at(terminal, pos_x+offset_x, pos_y+index+off_y, option_txt)

            # Bottom box
            bottom_txt = terminal.normal + '└' + "─"*(self._width-2) + '┘'
            print_at(terminal, pos_x+offset_x, pos_y+len(self._options)+off_y, bottom_txt)
        else:
            self._draw_selection_effect(terminal, pos_x, pos_y)


    @property
    def value(self):
        """ Actual chosen value """
        return self.options[self._opt_select][1]

    @property
    def value_text(self):
        """ Actual chosen value displayed """
        return self.options[self._opt_select][0]

    def handle_inputs(self, val, terminal):
        ret = self
        if self._choosing:
            match val.name:
                case "KEY_ENTER":
                    self._choosing = False
                    new_value = self._options[self._opt_select][1]
                    self._previous_choice = self._opt_select
                    print(terminal.clear)
                    ret = self._on_change(new_value)
                case "KEY_ESCAPE":
                    self._choosing = False
                    self._opt_select = self._previous_choice
                    print(terminal.clear)
                case "KEY_DOWN":
                    self._opt_select = (self._opt_select + 1) % len(self._options)
                case "KEY_UP":
                    self._opt_select = (self._opt_select - 1) % len(self._options)
        else:
            if val.name == "KEY_ENTER":
                self._choosing = True
                self._previous_choice = self._opt_select
            else:
                ret = super().handle_inputs(val, terminal)
        self._switch_to(ret)
        return ret
