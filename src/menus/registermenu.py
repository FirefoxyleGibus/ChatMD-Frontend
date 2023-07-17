"""
    RegisterMenu class file
"""
from src.app import App
from .loginmenu import LoginMenu

class RegisterMenu(LoginMenu):
    """ Register menu """

    def __init__(self):
        super().__init__("register")
        lang = App.get_instance().user_settings.get_locale()
        self._connect_button.set_text(lang.get("register"))

    def connect_button(self, username, password) -> str:
        """ Log in with a username and a password """
        return self._auth_request(App.get_instance().websocket.request_register, username, password)
