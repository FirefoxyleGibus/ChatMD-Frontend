import logging
from blessed import Terminal
from blessed.keyboard import Keystroke

from src.menus.ui_elements.base_selectable import BaseSelectable
from src.app import App
from src.termutil import print_at
from src.menus.ui_elements.text_style import TextStyle


class TextBox(BaseSelectable):
    """ Textbox """

    SIDES = {
        'down':  0,
        'up':    1,
    }

    def __init__(self, width: int, placeholder="text ...", prefix="", reverse_background=True, alignement: str = 'center', attachments: dict = None):
        super().__init__(attachments=attachments)
        self._text = ""
        self._curpos = 0
        self._width = width
        self._align = alignement
        self._placeholder = placeholder
        self._prefix = prefix
        self._reverse = reverse_background
    
    def handle_inputs(self, val: Keystroke, terminal: Terminal):
        ret = super().handle_inputs(val, terminal)
        len_text = len(self._text)
        match val.name:
            case "KEY_BACKSPACE" if self._text != "" and self._curpos > 0:
                self._text = self._text[:self._curpos] + self._text[self._curpos+1:]
                print(terminal.clear)
            case "KEY_LEFT":
                self._curpos = max(self._curpos - 1, 0)
            case "KEY_RIGHT":
                self._curpos = min(self._curpos + 1, len_text)
            case None if str(val):
                if self._curpos == 0:
                    self._text += str(val)
                    self._curpos += 1
                else:
                    self._text = self._text[:self._curpos] + str(val) + self._text[self._curpos:]
                    self._curpos += 1
        return ret

    def _draw_selected(self, terminal, pos_x, pos_y):
        pass

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the textbox """
        
        # Textbox draw
        text = self._prefix
        if len(self._text) == 0:
            text += terminal.darkgray(self._placeholder)
        else:
            text += self._text
            # scroll text left and right
            # if len(self._text) + len(self._prefix) > self._width:
            #     start_pos = max(self._curpos - (len(self._width) - len(self._prefix)), 0)
            #     end_pos = min(self._curpos, len(self._text))
            #     show_text = self._text[start_pos:end_pos]
        text, offset_x = TextStyle.align(terminal, self._align, text, self._width)

        formatted = (terminal.reverse if self._reverse else terminal.normal) \
            + terminal.normal_cursor                                         \
            + text                                                           \
            + terminal.normal + terminal.hide_cursor

        print_at(terminal, pos_x + offset_x, pos_y, formatted)

        # Draw cursor
        cursor_pos = pos_x + len(self._prefix) + self._curpos
        print_at(terminal, cursor_pos, pos_y, terminal.blink("_"))