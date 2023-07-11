"""
    Toggle button class file
"""

from src.termutil import print_at
from .button import Button
from .element_style import ElementStyle

class ToggleButton(Button):
    """ Toggle button class """
    _ACTIVE     = '[x]'
    _NOT_ACTIVE = '[ ]'

    _MARGIN = 2

    def __init__(self, forced_width=None, active=False, label="", attach: dict=None, style:ElementStyle=None):
        super().__init__("",
            attach=attach,
            width=forced_width if forced_width else len(label) + self._MARGIN * 2 + len(self._ACTIVE),
            style=style
        )
        self._active = active
        self._forced_width=forced_width
        self.set_on_click(self._toggle)
        self.set_text(label)

    def set_text(self, text):
        self._label = text.strip()
        if not self._forced_width:
            self._width = len(self._ACTIVE)
            if len(self._label) > 0:
                self._width += len(self._label) + 2 * self._MARGIN
        else:
            self._label = self._label[:min(self._forced_width-(self._MARGIN * 2 + len(self._ACTIVE)),0)]

    def _toggle(self):
        self._active = not self._active

    def draw(self, terminal, pos_x, pos_y):
        super()._draw_selection_effect(terminal, pos_x, pos_y)

        background = self._style.background(terminal)
        self._text = terminal.normal + self._label
        if len(self._label) > 0:
            self._text += ' '
        self._text += background + (self._ACTIVE if self._active else self._NOT_ACTIVE) + terminal.normal

        # draw label
        aligned,_ = self._style.align(terminal, self._text, self._width)
        offset_x = self._style.anchor_pos(self._width)

        print_at(terminal, pos_x+offset_x, pos_y, aligned)

    def active(self):
        """ Return true if active (toggled on) """
        return self._active
