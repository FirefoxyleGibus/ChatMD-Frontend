from src.termutil import *

class BaseMenu():
    turnOff = False

    def draw(self) -> None:
        pass

    def handle_input(self):
        val = term.inkey(timeout=1/60)
        return val

    def __init__(self) -> None:
        pass
