import json
import os

# Load onfiguration from JSON file
with open('config.json', 'r') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)


def INSTALLING_PACKAGES(package): # install packages
    try:
        os.system(f'pip install {package}')
    except Exception as ERROR:
        print(f"Error installating {package}.\n {ERROR}")


REQUIRED_PACKAGES = {'discord', 'flask', 'asyncio', 'qrcode[pil]', 'requests', 'colorama'} # required packages to install


if CONFIG.get("skip_installtion") == "false":
    for package in REQUIRED_PACKAGES: # loop and install required packages
        INSTALLING_PACKAGES(package)
else:
    from utilities import Fore, t
    print(f"{t}{Fore.RED} | Skipping Installtion of packages. {Fore.RESET}")
