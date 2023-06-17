import sys
import os
import subprocess

CONFIG_FILE = 'user_settings.yml'

def first_setup():
    # check if user_settings.yml exists
    if os.path.isfile(CONFIG_FILE):
        return

    # install libraries
    install_lib = lambda name: subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])
    with open('requirements.txt') as f:
        packages = f.readlines()
        for package in packages:
            if len(package) > 1:
                package = package.split(">")[0].split("<")[0].lstrip()
                print("Installing: ", package)
                install_lib(package)
        f.close()
