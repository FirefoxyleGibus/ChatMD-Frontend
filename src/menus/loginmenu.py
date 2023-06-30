"""
    LoginMenu class file
"""
import datetime

import json
import logging
import requests

from src.menus.basemenu import BaseMenu
from src.menus.ui_elements import TextBox, TextBoxPassword, Button, ElementStyle, ToggleButton
from src.termutil import print_at
from src.app import App
from src.menus.loginexception import LoginException
from src.bridge import Connection

class LoginMenu(BaseMenu):
    """ Login menu """

    def __init__(self):
        super().__init__("login")
        self.status_message = ""

        lang = App.get_instance().user_settings.get_locale()
        self._username = TextBox(40)

        self._password = TextBoxPassword(40, attach={'up': self._username})
        self._username.connect_side('down', self._password)

        self._connect_button = Button(lang.get("connect"), 20,
            attach={'up': self._password}).set_on_click(self._login_button)
        self._password.connect_side('down', self._connect_button)

        self._quit_button = Button(lang.get("quit"), 20,
            attach={'up': self._connect_button}).set_on_click(App.get_instance().quit)

        self._auto_connect = ToggleButton(label=lang.get('autoconnect'), attach={
            'up': self._connect_button,
            'down': self._quit_button
        })
        self._connect_button.connect_side('down', self._auto_connect)
        self._quit_button.connect_side('up', self._auto_connect)

        self._register_button = Button(lang.get("register"), 10,
            attach={'left': self._connect_button}, style={
                'anchor': 'right', 'align': 'center', 'background': True
            }
        ).set_on_click(App.get_instance().show_menu, 'register')
        self._connect_button.connect_side('right', self._register_button)
        self._auto_connect.connect_side('right', self._register_button)
        self._quit_button.connect_side('right', self._register_button)

    def start(self):
        self.focus_selectable(self._username)

        # Pre-load information of last-login
        user_settings = App.get_instance().user_settings
        
        # last login info
        username = user_settings.get("saved_username", None)
        if username:
            self._username.set_text(username)
        
        # Detect local token and keep signed in
        if user_settings.get("auto_connect", False):
            token = user_settings.get("session_token", None)
            if token and username:
                self._token_login(username, token)


    def login(self, username, password) -> str:
        """ Log in with a username and a password """
        if username.rstrip() != "" and password.rstrip() != "":
            try:
                response = requests.post(Connection.LOGIN_ENDPOINT,
                    data = {"username":username, "password":password}, timeout=5.0)
                full_response = json.loads(response.text)
                match full_response["code"]:
                    case 200:
                        return full_response["data"]["session"]
                    case 404:
                        raise LoginException("not_found")
                    case 418: # unknown user
                        raise LoginException("wrong_credentials")
                    case 401:
                        raise LoginException("wrong_credentials")
                    case _:
                        logging.error("Failed to connect: %d", full_response["code"])
                        raise LoginException("connection_fail")
            except json.JSONDecodeError:
                raise LoginException("connection_fail")
            except requests.exceptions.Timeout:
                raise LoginException("timeout")
            except requests.exceptions.TooManyRedirects:
                raise LoginException("connection_fail")
            except requests.exceptions.RequestException:
                raise LoginException("connection_fail")
        raise LoginException("missing_credentials")

    def draw(self, terminal) -> None:
        lang = App.get_instance().user_settings.get_locale()

        center_x, center_y = terminal.width//2, terminal.height//2

        welcome_text = lang.get("welcome_text")
        print_at(terminal, center_x-len(welcome_text)//2, center_y-5, welcome_text)
        print_at(terminal, center_x-len(self.status_message)//2, center_y-4,
            terminal.red(self.status_message))

        username = lang.get("username")
        print_at(terminal, center_x-len(username)//2, center_y-3, username)
        self._username.draw(terminal, center_x, center_y-2)

        password = lang.get("password")
        print_at(terminal, center_x-len(password)//2, center_y-1, password)
        self._password.draw(terminal, center_x, center_y)

        self._connect_button.draw(terminal, center_x, center_y+2)
        self._auto_connect.draw(terminal, center_x, center_y+4)
        self._quit_button.draw(terminal, center_x, center_y+6)

        self._register_button.draw(terminal, terminal.width - 8, center_y)

        date = datetime.datetime.now()

        date_message = lang.get('date_status').format(
                time=date.strftime('%H:%M:%S'), date=date.strftime('%A %d %B %Y'))
        print_at(terminal, 1,terminal.height-2, terminal.normal + date_message)

    def _login_button(self):
        user_settings = App.get_instance().user_settings
        lang = user_settings.get_locale()
        try:
            newtoken = self.login(self._username.text, self._password.text)
            self.status_message = ""

            # save token for auto connect
            user_settings.set("saved_username", self._username.text)
            if self._auto_connect.active():
                user_settings.set("auto_connect", True)
                user_settings.set("session_token", newtoken)
            else:
                user_settings.set("auto_connect", False)
                user_settings.set("session_token", None)

            self._token_login(self._username.text, newtoken)
        except LoginException as err:
            self._password.set_text('') # clear text
            self.status_message = lang.get(err.get_failure())
    
    def _token_login(self, username, token):
        app = App.get_instance()
        app.token = token
        app.show_menu("chat")
        app.get_menu("chat").name = username
        app.get_menu("chat").connect(app.token)

    def handle_input(self, terminal) -> None:
        val = super().handle_input(terminal)
        if self._connect_button.is_selected and val.name == "KEY_ENTER":
            print(terminal.clear)
