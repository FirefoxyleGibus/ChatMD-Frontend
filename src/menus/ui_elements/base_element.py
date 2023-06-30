"""
    Base Element
"""

from src.menus.ui_elements.element_style import ElementStyle

class BaseElement():
    def __init__(self, width, style=None):
        self._width = width
        self._style = style if style else ElementStyle({})

    def draw(self, _terminal, _pos_x, _pos_y):
        """ Draw the element """
        return