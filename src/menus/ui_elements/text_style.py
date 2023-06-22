from blessed import Terminal

class TextStyle():
    """ Class utils to style text """
    @staticmethod
    def align(terminal: Terminal, align: str, text: str, width: int) -> str:
        """ Return aligned text to be drawn correctly """
        match align:
            case 'left':
                return terminal.ljust(text, width), 0
            case 'right':
                return terminal.rjust(text, width), width-len(text)+1
            case 'center':
                return terminal.center(text, width), width//2-len(text)//2
        return text, 0
    
    @staticmethod
    def anchor_pos(anchor, width):
        """ Return the offset pos for a specified anchor """
        match anchor:
            case 'left':
                return -width
            case 'right':
                return  width+1
            case 'center':
                return  -width//2
        return 0