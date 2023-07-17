"""
    Terminal utilities:
    - print_at
    - color_text
    - prng
    - color_code_from_hex
    - hexcode_from_color_code
"""

# shamelessly stolen from HastagGuigui/shellrhythm, by HastagGuigui himself

def print_at(terminal, pos_x, pos_y, text):
    """ Print something at a position in the terminal """
    print(terminal.move_xy(int(pos_x), int(pos_y)) + text)
