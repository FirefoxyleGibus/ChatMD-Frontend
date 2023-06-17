
class Locale:
    def __init__(self, locale_name):
        self._words={}
        data = []
        with open(f'locales/{locale_name}') as f:
            data = f.readlines()
            f.close()
        
        for line in data:
            var,traduction = line.split('=')
            self._words[var] = traduction.rstrip()
            
    def get(self, word):
        return self._words.get(word, str(word))
