"""" User preferences subpackage """
__all__ = ["locales", "user_settings"]

import os
import sys
import subprocess


CONFIG_FILE = 'user_settings.yml'

def first_setup():
    """
    Setup libraries (install or update) and config file on startup
    """
    # install or update libraries
    # check if user_settings.yml exists
    if not os.path.isfile(CONFIG_FILE):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    else:
        config_mtime = os.path.getmtime(CONFIG_FILE)
        requirements_mtime = os.path.getmtime('requirements.txt')
        if config_mtime < requirements_mtime: # update
            subprocess.check_call([sys.executable,'-m','pip','install','-r','requirements.txt'])
