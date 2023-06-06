# Ceci est la technique du "on évite un crash si l'on démarre un des scripts internes au lieu du vrai script même si bon on s'en branle"
try:
    from src.termutil import *
except ImportError:
    from termutil import * 

class BaseMenu():
    turnOff = False

    def draw(self) -> None:
        pass

    def handle_input(self):
        val = term.inkey(timeout=1/60)
        return val

    def __init__(self) -> None:
        pass
