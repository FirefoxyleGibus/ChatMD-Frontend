"""
    Profile menu class file
"""

import logging
import requests

from src.app import App
from src.termutil import print_at
from .basemenu import BaseMenu
from ..user_prefs import Locale
from .ui_elements import Button, TextBox, DropDown, ElementStyle

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
        )

        self._username.connect_side('down', self._lang)
        self._username.connect_side('next', self._lang)

        self._save_button = Button(lang.get("save"), 40).set_on_click(self._save)
        self._save_button.connect_side('up', self._lang)
        self._save_button.connect_side('prev', self._lang)
        self._save_status = ""

        self._lang.connect_side('down', self._save_button)
        self._lang.connect_side('next', self._save_button)

        self._quit_button = Button(lang.get("quit"), 40,
            attach={
                'left': self._save_button, 'prev': self._save_button
            }).set_on_click(self._quit)
        self._save_button.connect_side('right', self._quit_button)
        self._save_button.connect_side('next', self._quit_button)

    def start(self):
        self.focus_selectable(self._username)

    def set_lang(self, lang):
        """ Set lang selected """
        logging.debug("locale: %s from %s", lang, self._lang.options)
        self._lang.set_choosing(False, self._available_lang.index(lang))

    def set_username(self, username):
        """ Set actual username """
        self._username.set_text(username)

    def _save(self):
        app = App.get_instance()
        # save text / update
        if self._username.text.strip() != "":
            # database update username
            if self._update_username_to_db():
                app.user_settings.set("username", self._username.text)
                # app.get_menu("chat").name = self._username.text
            else:
                self._username.set_text(app.get_menu("chat").name)
                logging.error("Failed to change username")
        # save locale
        app.user_settings.set("locale", self._lang.value)
        return self

    def _update_username_to_db(self):
        lang = App.get_locale()
        try:
            self._save_status = ''
            res = App.get_instance().websocket.request_update_username(self._username.text)
            logging.info("Updated Username : %s ", repr(res))
            if res.status_code == 200:
                self._save_status = "{cf 00FF00}" + lang.get("profile_saved")
                return True
            logging.error("Failed to save profile : %s", res)
            self._save_status = "{cf FF0000}" + lang.get("profile_failed_save")
            return False
        except requests.exceptions.Timeout:
            self._save_status = "{cf FF0000}" + lang.get("timeout")
            return False
        except requests.exceptions.TooManyRedirects:
            self._save_status = "{cf FF0000}" + lang.get("connection_fail")
            return False
        except requests.exceptions.RequestException:
            self._save_status = "{cf FF0000}" + lang.get("connection_fail")
            return False

    def _quit(self):
        App.get_instance().show_menu("chat")

    def draw(self, terminal):
        lang = App.get_locale()

        center_x = terminal.width//2
        center_y = terminal.height//2

        # error/status
        status_text = ElementStyle.color_text(terminal, self._save_status)
        print_at(terminal, 0, center_y-4, terminal.center(status_text) + terminal.normal)

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
