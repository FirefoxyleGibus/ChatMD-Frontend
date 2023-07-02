"""
    ElementStyle and Color file
"""

from blessed import Terminal

def prng (beat = 0.0, seed = 0):
    """ Random gen """ 
    # quick pseudorandomness don't mind me
    return int(beat * 210413 + 2531041 * (seed+1.3)/3.4) % 2**32

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
    def color_text(terminal, text, beat = 0.0):
        """ Color fancy display text 
            Here, replace something like {cf XXXXXX} with the corresponding terminal color
            Combinaisons supported: 
            - cf RRGGBB        Foreground color
            - cb RRGGBB        Background color
            - b                Bold text
            - i                Italic text
            - u                Underline text
            - n                Reverts text back to normal state
            - r                Flips foreground and background
            - k                Glitchifies text
        """
        text = text.replace(r"\\{", "￼ø").replace(r"\\}", "ŧ￼").replace("{", "�{").replace("}", "}�")
        # If you are using � or "￼" genuiunely, what the #### is wrong with you /gen
        data = text.split("�")
        rendered_text = ""
        glitchify_next = False
        for i in data:
            if i.startswith("{") and i.endswith("}"):
                code = i.strip("{}")
                match code:
                    case "b":
                        rendered_text += terminal.bold
                        continue
                    case "i":
                        rendered_text += terminal.italic
                        continue
                    case "u":
                        rendered_text += terminal.underline
                        continue
                    case "n":
                        rendered_text += terminal.normal
                        glitchify_next = False
                        continue
                    case "r":
                        rendered_text += terminal.reverse
                        continue
                    case "k":
                        glitchify_next = True
                        continue
                    case _ if code.startswith("cb"):
                        col = color_code_from_hex(code.replace("cb ", "", 1))
                        rendered_text += terminal.on_color_rgb(col[0], col[1], col[2])
                        continue
                    case _ if code.startswith("cf"):
                        col = color_code_from_hex(code.replace("cf ", "", 1))
                        rendered_text += terminal.color_rgb(col[0], col[1], col[2])
                        continue
                    case _ if glitchify_next:
                        #this big chunk will generate a random string with characters from 0x20 to 0x7e
                        rendered_text += "".join([
                            chr(int(prng(beat, k))%(0x7e-0x20) + 0x20)
                            for k in range(len(i.replace("￼ø", "{").replace("ŧ￼", "}")))
                        ])
                    case _:
                        rendered_text += i.replace("￼ø", "{").replace("ŧ￼", "}")
            else:
                if glitchify_next:
                    rendered_text += "".join([
                        chr(int(prng(beat, k))%(0x7e-0x20) + 0x20)
                        for k in range(len(i.replace("￼ø", "{").replace("ŧ￼", "}")))
                    ])
                else:
                    rendered_text += i.replace("￼ø", "{").replace("ŧ￼", "}")
        return rendered_text

    @staticmethod
    def add_background(terminal, text):
        """ Add a background to the text """
        return terminal.reverse + text + terminal.normal

    @staticmethod
    def create_with_defaults(defaults:dict, new_value:dict):
        """ Create the element style using a default dict and a value dict
            replacing defaults with values in value dict.
        """
        if new_value is None: return ElementStyle(defaults)

        value = defaults
        for name,val in new_value.items():
            value[name] = val
        return ElementStyle(value)

class Color():
    """ Color class """

    @staticmethod
    def color_code_from_hex(hexcode:str) -> list:
        """ Converts hexcode 'RRGGBB' to color code """
        # hexcode is string built like "RRGGBB"
        output = [0,0,0]
        if len(hexcode) == 6: #No more, no less
            try:
                output = [int(hexcode[i:i+2], 16) for i in range(0, len(hexcode), 2)]
            except ValueError:
                pass
        return output

    @staticmethod
    def hexcode_from_color_code(code:list) -> str:
        """ Converts color code to hexcode 'RRGGBB' """
        output = "000000"
        if len(code) == 3:
            output = hex((code[0] * 256**2) + (code[1] * 256) + code[2]).replace("0x", "")
        if len(output) < 6:
            output = "0"*(6-len(output)) + output
        return output