"""
Runs when main.py is ran
All this does is installs required libraries
You can disable this from running every time main.py runs
by changing 'skip_installation' to 'true' in the config
Note: when installation a new release, be sure to check
that there aren't any new dependencies.
"""

import json
import os

# Load onfiguration from JSON file
with open('config.json', 'r') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)

def SETUP_INSTALL():
    def INSTALLING_PACKAGES(package): # install packages
        try:
            os.system(f'pip install {package}')
        except Exception as ERROR:
            print(f"Error installating {package}.\n {ERROR}")


    REQUIRED_PACKAGES = {'discord', 'flask', 'asyncio', 'qrcode[pil]', 'requests', 'colorama', 'aiohttp==3.7.4.post0', 'async-timeout==3.0.1', 'chardet==4.0.0', 'chardet==4.0.0', 'idna==3.1', 'multidict==5.1.0', 'pillow', 'typing-extensions==3.7.4.3', 'yarl'} # required packages to install


    if CONFIG.get("skip_installtion") == "false":
        os.system('pip install git+https://github.com/Rapptz/discord.py') # for discord.ui 

        for package in REQUIRED_PACKAGES: # loop and install required packages
            INSTALLING_PACKAGES(package)
    else:
        from utilities import Fore, t
        print(f"{t}{Fore.RED} | Skipping Installtion of packages. {Fore.RESET}")
