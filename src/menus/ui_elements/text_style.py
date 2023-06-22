from blessed import Terminal

class TextStyle():
    """ Class utils to style text """
    @staticmethod
    def align(terminal: Terminal, align: str, text: str, width: int) -> tuple[str, int]:
        """ Return aligned text and the offset to be drawn correctly """
        match align:
            case 'left':
                return terminal.ljust(text, width), -width
            case 'right':
                return terminal.rjust(text, width), width+1
            case ('center'|_):
                return terminal.center(text, width), 0
        return text,0