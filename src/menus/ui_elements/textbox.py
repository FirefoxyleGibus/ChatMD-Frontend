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

    def __init__(self, width: int, placeholder="text ...", prefix="", reverse_background=True, anchor='center', align: str = 'center', attach: dict = None):
        super().__init__(attachments=attach, clear_terminal_move=False)
        self._text = ""
        self._curpos = 0
        self._width = width
        self._anchor = anchor
        self._align = align
        self._placeholder = placeholder
        self._prefix = prefix
        self._reverse = reverse_background

    def handle_inputs(self, val: Keystroke, terminal: Terminal):
        ret = super().handle_inputs(val, terminal)
        match val.name:
            case "KEY_BACKSPACE" if self._text != "" and self._curpos > 0:
                self._text = self._text[:self._curpos-1] + self._text[self._curpos:]
                self._curpos -= 1
                # print(terminal.clear)
            case "KEY_LEFT":
                self._curpos = max(self._curpos - 1, 0)
            case "KEY_RIGHT":
                self._curpos = min(self._curpos + 1, len(self._text))
            case None if str(val):
                if self._curpos == 0:
                    self._text += str(val)
                    self._curpos += 1
                else:
                    self._text = self._text[:self._curpos] + str(val) + self._text[self._curpos:]
                    self._curpos += 1
        return ret

    def _get_shown_text(self, _terminal):
        """ Return the text to show on screen """
        # Textbox draw
        text = self._prefix
        if len(self._text) == 0 and not self.is_selected:
            text += self._placeholder
        else:
            show_text = self._text
            # scroll text left and right if overflow
            if len(self._text) + len(self._prefix) > self._width:
                start_pos = max(self._curpos - (self._width - len(self._prefix)), 0)
                end_pos = min(self._curpos, len(self._text))
                show_text = self._text[start_pos:end_pos]
            text += show_text
        return text

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the textbox """
        background = (terminal.reverse if self._reverse else terminal.normal)
        text, left_char_pos = TextStyle.align(terminal, self._align, self._get_shown_text(terminal), self._width)
        offset_x = TextStyle.anchor_pos(self._anchor, self._width)
        formatted = background + text + terminal.normal
        print_at(terminal, pos_x + offset_x, pos_y, formatted)

        # Draw cursor
        if len(self._text) != 0 or self.is_selected:
            cursor_pos = pos_x + min(self._curpos, self._width - len(self._prefix) - 1) \
                + len(self._prefix) + offset_x + left_char_pos
            print_at(terminal, cursor_pos, pos_y, background + terminal.blink("_") + terminal.normal)