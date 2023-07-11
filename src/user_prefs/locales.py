"""
    Locale class file
"""
import os
import locale

class Locale:
    """ Languages translation """
    def __init__(self, locale_name):
        self._words={}
        self._locale_name = locale_name
        self.reload()

        locale.setlocale(locale.LC_ALL, '')

    def reload(self):
        """ Reload the locale file and reparse it """
        data = []
        with open(f'locales/{self._locale_name}', 'r', encoding='utf-8') as file:
            data = file.readlines()
            file.close()

        for line in data:
            if line.rstrip().lstrip() != "":
                var,traduction = line.split('=')
                self._words[var] = traduction.rstrip()

    def get(self, word):
        """ Get the translated word in this locale or the original word """
        return self._words.get(word, str(word))

    @staticmethod
    def get_available():
        """ Get available locales """
        return os.listdir('locales/')
