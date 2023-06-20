from blessed import *
from blessed.keyboard import *

# shamelessly stolen from HastagGuigui/shellrhythm, by HastagGuigui himself

def print_at(terminal, x, y, text):
    """ Print something at a position in the terminal """
    print(terminal.move_xy(int(x), int(y)) + text)

def prng (beat = 0.0, seed = 0):
    """ Random gen """ 
    # quick pseudorandomness don't mind me
    return int(beat * 210413 + 2531041 * (seed+1.3)/3.4) % 2**32

def color_text(term, text = "", beat = 0.0):
    """ Color fancy display text """
    #Here, replace something like {cf XXXXXX} with the corresponding terminal color
    #Combinaisons to support: 
    # - cf RRGGBB		Foreground color
    # - cb RRGGBB		Background color
    # - b				Bold text
    # - i				Italic text
    # - u				Underline text
    # - n				Reverts text back to normal state
    # - r				Flips foreground and background
    # - k				Glitchifies text

    text = text.replace("\{", "￼ø").replace("\}", "ŧ￼").replace("{", "�{").replace("}", "}�")
    #If you are using � or "￼" genuiunely, what the #### is wrong with you /gen
    data = text.split("�")
    rendered_text = ""
    glitchify_next = False
    for i in data:
        if i.startswith("{") and i.endswith("}"):
            ac = i.strip("{}")
            if ac.startswith("cf"):
                col = color_code_from_hex(ac.replace("cf ", "", 1))
                rendered_text += term.color_rgb(col[0], col[1], col[2])
                continue
            if ac.startswith("cb"):
                col = color_code_from_hex(ac.replace("cb ", "", 1))
                rendered_text += term.on_color_rgb(col[0], col[1], col[2])
                continue
            if ac == "b":
                rendered_text += term.bold
                continue
            if ac == "i":
                rendered_text += term.italic
                continue
            if ac == "u":
                rendered_text += term.underline
                continue
            if ac == "n":
                rendered_text += term.normal
                glitchify_next = False
                continue
            if ac == "r":
                rendered_text += term.reverse
                continue
            if ac == "k":
                glitchify_next = True
                continue
            if glitchify_next:
                #this big chunk will generate a random string with characters from 0x20 to 0x7e
                rendered_text += "".join([chr(int(prng(beat, k))%(0x7e-0x20) + 0x20) for k in range(len(i.replace("￼ø", "{").replace("ŧ￼", "}")))])
            else:
                rendered_text += i.replace("￼ø", "{").replace("ŧ￼", "}")
        else:
            if glitchify_next:
                rendered_text += "".join([chr(int(prng(beat, k))%(0x7e-0x20) + 0x20) for k in range(len(i.replace("￼ø", "{").replace("ŧ￼", "}")))])
            else:
                rendered_text += i.replace("￼ø", "{").replace("ŧ￼", "}")
    return rendered_text

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

def hexcode_from_color_code(code:list) -> str:
    """ Converts color code to hexcode 'RRGGBB' """
    output = "000000"
    if len(code) == 3:
        output = hex((code[0] * 256**2) + (code[1] * 256) + code[2]).replace("0x", "")
    if len(output) < 6:
        output = "0"*(6-len(output)) + output
    return output

def textbox_logic(cur_text, cursor_pos, val) -> tuple[str, int]:
    """ Textbox input """
    if val.name == "KEY_BACKSPACE":
        if cur_text != "":
            cur_text = cur_text[:len(cur_text)-(cursor_pos+1)] + cur_text[len(cur_text)-cursor_pos:]
    elif val.name == "KEY_LEFT":
        cursor_pos = min(cursor_pos + 1, len(cur_text))
    elif val.name == "KEY_RIGHT":
        cursor_pos = max(cursor_pos - 1, 0)
    else:
        if val.name is None:
            if cursor_pos == 0:
                cur_text += str(val)
            else:
                cur_text = cur_text[:len(cur_text)-cursor_pos] + str(val) + cur_text[len(cur_text)-cursor_pos:]
    
    return cur_text, cursor_pos
