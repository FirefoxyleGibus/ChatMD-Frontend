import locale

class Locale:
    """ Languages translation """
    def __init__(self, locale_name):
        self._words={}
        data = []
        with open(f'locales/{locale_name}', 'r', encoding='utf-8') as f:
            data = f.readlines()
            f.close()
        
        for line in data:
            if line.rstrip().lstrip() != "":
                var,traduction = line.split('=')
                self._words[var] = traduction.rstrip()

        locale.setlocale(locale.LC_ALL, '')

        
            
    def get(self, word):
        """ Get the translated word in this locale or the original word """
        return self._words.get(word, str(word))
