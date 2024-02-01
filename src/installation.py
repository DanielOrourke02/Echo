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


    REQUIRED_PACKAGES = {'discord', 'flask', 'asyncio', 'qrcode[pil]', 'requests', 'colorama', 'aiohttp==3.7.4.post0', 'async-timeout==3.0.1', 'chardet==4.0.0', 'chardet==4.0.0', 'idna==3.1', 'multidict==5.1.0', 'Pillow==8.2.0', 'typing-extensions==3.7.4.3', 'yarl==1.6.3'} # required packages to install


    if CONFIG.get("skip_installtion") == "false":
        for package in REQUIRED_PACKAGES: # loop and install required packages
            INSTALLING_PACKAGES(package)
    else:
        from utilities import Fore, t
        print(f"{t}{Fore.RED} | Skipping Installtion of packages. {Fore.RESET}")
