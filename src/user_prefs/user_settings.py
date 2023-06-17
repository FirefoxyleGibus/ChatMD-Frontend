from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from src.user_prefs import CONFIG_FILE
import os

from src.user_prefs.locales import Locale

class UserSettings:

    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            file = open(CONFIG_FILE, 'w')
            file.write('setup: yes')
            file.close()

        self._file = open(CONFIG_FILE, 'r')
        self._content = load(self._file, Loader=Loader)
        self._file.close()
        
        if not 'locale' in self._content.keys():
            self.set('locale', 'en_US')
        self._locale = Locale(self._content['locale'])

        UserSettings.current = self

    def reload_locale(self):
        self._locale = Locale(self._content['locale'])

    def get_locale(self):
        return self._locale 

    def get(self, name, default=None) -> any:
        return self._content.get(name, default)
    
    def set(self, name, value):
        self._content[name] = value
        self._file = open(CONFIG_FILE, 'w')
        dump(self._content, self._file)
        self._file.close()

    def get_current():
        return UserSettings.current
