"""
    Callback wrapper class
"""

import logging

class Callback():
    """" Callback wrapper """
    def __init__(self, default:callable=lambda *args, **kwargs: None):
        self._callback : callable = default
        self._args     : tuple = ()
        self._kwargs   : dict  = {}
    
    def call(self, *args):
        """ Call the callback """
        return self._callback(*args, *self._args, **self._kwargs)
    
    def set_func(self, callback, *args, **kwargs):
        """ Update callback """
        self._callback = callback.__call__
        self._args = args
        self._kwargs = kwargs