"""
    Base Element
"""

from .element_style import ElementStyle

class BaseElement():
    """ Base element """
    def __init__(self, width, style=None):
        self._width = width
        self._style = style if style else ElementStyle({})

    def draw(self, _terminal, _pos_x, _pos_y):
        """ Draw the element """
        return

    @property
    def width(self) -> int:
        """ Width of the element """
        return self._width
