"""
    UserSettings class file
"""
import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from src.user_prefs import CONFIG_FILE

from .locales import Locale

class UserSettings:
    """ User settings """
    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
                file.write('setup: yes')
                file.close()

        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            self._content = load(file, Loader=Loader)
            file.close()

        if not 'locale' in self._content.keys():
            self.set('locale', 'en_US')
        self._locale = Locale(self._content['locale'])

        UserSettings.current = self

    def reload_locale(self):
        """ Reload the locale of the user using the specified locale in settings """
        self._locale = Locale(self._content['locale'])

    def get_locale(self):
        """ Get the current local of this user """
        return self._locale

    def get(self, name, default=None) -> any:
        """ Get the settings 'name' set by this user  """
        return self._content.get(name, default)

    def set(self, name, value):
        """ Set the settings 'name' for this user  """
        self._content[name] = value
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            dump(self._content, file, Dumper=Dumper)
            file.close()

    @staticmethod
    def get_current():
        """ Get current used User Settings """
        return UserSettings.current
