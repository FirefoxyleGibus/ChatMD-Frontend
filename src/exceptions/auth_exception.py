"""
    Authentification Exception
"""

class AuthException(Exception):
    """ Exception for auth (login or register) """
    def __init__(self, failure):
        super().__init__()
        self._failure = failure

    def get_failure(self):
        """ Return the failure reason """
        return self._failure
