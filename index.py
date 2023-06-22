"""
    Install missing libraries on first
    Startup and load user settings
"""
from src.user_prefs import first_setup
try:
    from src import main
except ImportError:
    first_setup()
    from src import main

if __name__ == "__main__":
    first_setup()
    main()
