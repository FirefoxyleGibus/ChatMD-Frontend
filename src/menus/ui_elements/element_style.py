"""
    ElementStyle file class
"""

from blessed import Terminal

class ElementStyle():
    """ UI Element style """

    _defined_style_propreties = {
        "align": 'left',
        "anchor": 'left',
        "color": '',
        "background": False
    }
    """ Defined style propreties and their default values """

    def __init__(self, style: dict):
        self._style = {}
        for key,val in self._defined_style_propreties.items():
            self._style[key] = style.get(key, val)

    def align(self, terminal: Terminal, text: str, width: int) -> tuple[str, int]:
        """ Return aligned text to be drawn correctly + left char pos """
        match self._style.get("align", 'left'):
            case 'left':
                return terminal.ljust(text, width), 0
            case 'right':
                return terminal.rjust(text, width), width-len(text)+1
            case 'center':
                return terminal.center(text, width), width//2-(len(text)+1)//2
        return text, 0

    def anchor_pos(self, width):
        """ Return the offset pos for a specified anchor """
        match self._style.get("anchor", 'left'):
            case 'left':
                return  0
            case 'right':
                return  -width
            case 'center':
                return  -width//2
        return 0

    def get(self, style_proprety):
        """ Get the value of a style proprety """
        if style_proprety in self._defined_style_propreties:
            return self._style[style_proprety]
        return None

    def set(self, style_proprety, new_value):
        """ Set the value of a style proprety """
        if style_proprety in self._defined_style_propreties:
            self._style[style_proprety] = new_value

    def background(self, terminal):
        """ Return background code """
        return terminal.reverse if self._style["background"] else terminal.normal

    @staticmethod
    def create_with_defaults(defaults:dict, new_value:dict):
        if new_value is None: return ElementStyle(defaults)

        value = defaults
        for name,val in new_value.items():
            value[name] = val
        return ElementStyle(value)