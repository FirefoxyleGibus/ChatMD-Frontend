from src.menus.ui_elements.textbox import TextBox
from src.menus.ui_elements.text_style import TextStyle
from src.menus.ui_elements.button import Button

class TextBoxPassword(TextBox):
    """ password Textbox """

    def __init__(self, width: int, prefix="", reverse_background=True, anchor="center", align='center', attach=None):
        super().__init__(width, "", prefix, reverse_background, anchor, align, attach)
        self._width -= 4 # space for toggle_button
        self.hidden = True
        self._toggle_button = Button('[ ]', 3, anchor='left', align='right', attach={'up': self})\
            .set_on_click(self._toggle_visibility)
        self._attachments[self.SIDES.get('down')] = self._toggle_button

    def _toggle_visibility(self):
        if self.hidden:
            self._toggle_button.set_text("[x]")
            self.hidden = False
        else:
            self._toggle_button.set_text("[ ]")
            self.hidden = True

    def connect_side(self, side: str, element) -> None:
        """ Connect a textboxpassword to a side """
        if side in self.SIDES:
            if side == 'down':
                self._toggle_button.connect_side('down', element)
            else:
                self._attachments[self.SIDES[side]] = element

    def _get_shown_text(self, _terminal):
        """ Return the text to show on screen """
        # Textbox draw
        text = self._prefix
        if not (len(self._text) == 0 and not self.is_selected):
            show_text = self._text
            # scroll text left and right if overflow
            if len(self._text) + len(self._prefix) > self._width:
                start_pos = max(self._curpos - (self._width - len(self._prefix)), 0)
                end_pos = min(self._curpos, len(self._text))
                show_text = self._text[start_pos:end_pos]
            text += "*"*len(show_text) if self.hidden else show_text
        return text
    
    def draw(self, terminal, pos_x, pos_y):
        """ Draw the text box password """
        super().draw(terminal, pos_x, pos_y)

        offset_x = TextStyle.anchor_pos(self._anchor, self._width)
        # draw button
        self._toggle_button.draw(terminal, pos_x + offset_x + self._width + 4, pos_y)