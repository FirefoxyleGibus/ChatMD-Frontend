"""
    Profile menu class file
"""

import logging

from src.app import App
from src.termutil import print_at
from .basemenu import BaseMenu
from ..user_prefs import Locale
from .ui_elements import Button, TextBox, DropDown

class ProfileMenu(BaseMenu):
    """ Profile menu class """

    SIZE = 20

    def __init__(self):
        super().__init__("profile")

        lang = App.get_locale()

        self._username = TextBox(40, placeholder='')
        self._available_lang = Locale.get_available()
        self._lang = DropDown(40, options=[
                (lang, lang)
                for lang in self._available_lang
            ], 
            attachments={'up': self._username, 'prev': self._username}
        ).set_on_change(self._change_locale)

        self._username.connect_side('down', self._lang)
        self._username.connect_side('next', self._lang)

        self._save_button = Button(lang.get("save"), 40).set_on_click(self._save)
        self._save_button.connect_side('up', self._lang)
        self._save_button.connect_side('prev', self._lang)

        self._lang.connect_side('down', self._save_button)
        self._lang.connect_side('next', self._save_button)

        self._quit_button = Button(lang.get("quit"), 40,
            attach={
                'left': self._save_button, 'prev': self._save_button
            }).set_on_click(self._quit)
        self._save_button.connect_side('right', self._quit_button)
        self._save_button.connect_side('next', self._quit_button)

    def start(self):
        logging.debug("Showing profile :)")
        self.focus_selectable(self._username)

    def set_lang(self, lang):
        logging.debug("locale: %s from %s", lang, self._lang.options)
        self._lang.set_choosing(False, self._available_lang.index(lang))

    def set_username(self, username):
        self._username.set_text(username)

    def _change_locale(self, lang):
        App.get_instance().user_settings.set("locale", lang)

    def _save(self):
        # Update username on db + chatmenu
        # Save on usersettings + Update lang (force reload or notify user ?)
        return

    def _quit(self):
        App.get_instance().show_menu("chat")

    def draw(self, terminal):
        lang = App.get_locale()

        center_x = terminal.width//2
        center_y = terminal.height//2

        # title
        print_at(terminal, 0, 0, terminal.center(lang.get("profile")))

        # separation
        print_at(terminal, 0, 1, "─"*terminal.width)

        # username
        print_at(terminal, 0, center_y-2, terminal.center(lang.get("username")))
        self._username.draw(terminal, center_x, center_y)

        # lang/locale
        print_at(terminal, 0, center_y+2, terminal.center(lang.get("language")))
        self._lang.draw(terminal, center_x, center_y+4)

        # buttons
        self._save_button.draw(terminal, center_x-22, terminal.height - 2)
        self._quit_button.draw(terminal, center_x+22, terminal.height - 2)
