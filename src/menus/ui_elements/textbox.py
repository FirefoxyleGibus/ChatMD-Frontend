"""
    TextBox class file
"""
from blessed import Terminal
from blessed.keyboard import Keystroke

from src.menus.ui_elements.base_selectable import BaseSelectable
from src.menus.ui_elements.element_style import ElementStyle
from src.termutil import print_at

class TextBox(BaseSelectable):
    """ Textbox """

    SIDES = {
        'down':  0,
        'up':    1,
    }

    def __init__(self, width: int, placeholder="", prefix="", style=None, attach: dict = None):
        super().__init__(width, style=ElementStyle.create_with_defaults({
            'align': 'center', 'anchor': 'center', 'background': True
        }, style), attachments=attach, clear_terminal_move=False)
        self._text = ""
        self._curpos = 0
        self._placeholder = placeholder
        self._prefix = prefix

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
                    self._text = str(val) + self._text
                    self._curpos += 1
                else:
                    self._text = self._text[:self._curpos] + str(val) + self._text[self._curpos:]
                    self._curpos += 1
        self._curpos = max(min(self._curpos, len(self._text)), 0)
        return ret

    def resize(self, width: int) -> None:
        """ Resize the element """
        self._width = width

    @property
    def text(self) -> str:
        """ Return the text of this textbox """
        return self._text

    def set_text(self, new_text: str) -> None:
        """ Set the content of this textbox """
        self._text = new_text

    def _visible_text(self):
        return self._text

    def _get_shown_text(self, _terminal):
        """ Return the text to show on screen """
        # Textbox draw
        text = self._prefix
        if len(self._text) == 0 and not self.is_selected:
            text += self._placeholder
        else:
            visible_text = self._visible_text()

            show_text = visible_text
            # scroll text left and right if overflow
            if len(visible_text) + len(self._prefix) + 1 > self._width:
                start_pos = max(self._curpos - (self._width - len(self._prefix)-1), 0)
                end_pos = max(min(
                    self._curpos, len(visible_text)),
                    (self._width - len(self._prefix)-1
                ))
                show_text = visible_text[start_pos:end_pos]
            text += show_text
        return text

    def draw(self, terminal: Terminal, pos_x: int, pos_y: int):
        """ Draw the textbox """

        background = self._style.background(terminal)
        rendered_text = self._get_shown_text(terminal)
        text, left_char_pos = self._style.align(terminal, rendered_text, self._width)
        offset_x = self._style.anchor_pos(self._width)
        formatted = background + text + terminal.normal
        print_at(terminal, pos_x + offset_x, pos_y, formatted)

        # Draw cursor
        if self.is_selected:
            cursor_pos = pos_x + min(self._curpos, self._width - len(self._prefix) - 1) \
                + len(self._prefix) + offset_x + left_char_pos
            cursor_char = self._visible_text()[self._curpos] \
                if self._curpos < len(self._visible_text()) else " "
            print_at(terminal, cursor_pos, pos_y,
                background + terminal.underline(cursor_char) + terminal.normal)
