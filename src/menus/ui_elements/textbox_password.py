from src.menus.ui_elements.textbox import TextBox
from src.menus.ui_elements.text_style import TextStyle
from src.menus.ui_elements.button import Button

class TextBoxPassword(TextBox):
    """ password Textbox """

    def __init__(self, width: int, prefix="", reverse_background=True, anchor="center", align='center', attach=None):
        super().__init__(width, "", prefix, reverse_background, anchor, align, attach)
        # self._width -= 4 # space for toggle_button
        self._hidden_text = ""
        self._hidden = True
        self._toggle_button = Button('[ ]', 3, anchor='left', align='right', attach={'up': self})\
            .set_on_click(self._toggle_visibility)
        self._attachments[self.SIDES.get('down')] = self._toggle_button

    def _toggle_visibility(self):
        if self._hidden:
            self._toggle_button.set_text("[x]")
            self._hidden = False
        else:
            self._toggle_button.set_text("[ ]")
            self._hidden = True
    
    def _visible_text(self):
        if self._hidden:
            return '*'*len(self._text)
        return self._text

    def connect_side(self, side: str, element) -> None:
        """ Connect a textboxpassword to a side """
        if side in self.SIDES:
            if side == 'down':
                self._toggle_button.connect_side('down', element)
            else:
                self._attachments[self.SIDES[side]] = element
    
    def draw(self, terminal, pos_x, pos_y):
        """ Draw the text box password """
        super().draw(terminal, pos_x, pos_y)

        # draw button
        offset_x = TextStyle.anchor_pos(self._anchor, self._width)
        self._toggle_button.draw(terminal, pos_x + offset_x + self._width + 4, pos_y)