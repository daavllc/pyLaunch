import webbrowser
import os
import sys
import subprocess
import json

import helpers.config as config

from frontend.setup import Setup

class Launch:
    def __init__(self):
        self.PyPath = None

    def Automatic(self):
        self.PyPath = GetPython()
        if self.PyPath is None:
            print(f"Uh oh, we couldn't find the required python version...")
            print(f"Please install Python {config.USER_CONFIGURATION['Setup']['PythonVersion']} and try again")
            if 'y' in input("Open webrowser to download? (y/N) > "):
                webbrowser.open("https://www.python.org/downloads/")
            input("Press enter to exit")
            sys.exit(0)
        print(f"Using Python at: {self.PyPath}")

        # Run setup script and install required packages
        Setup(self.PyPath)
        self.pyLaunch()

    def Initialize(self) -> bool:
        self.PyPath = GetPython()
        if self.PyPath is None:
            return False
        return True

    def pyLaunch(self):
        ReturnValue = None
        UserCodes = []
        UserArgs = []
        for key, value in config.USER_CONFIGURATION['Launch'].items():
            try:
                key = int(key) # If key is integer, it's a return code
            except ValueError:
                continue
            UserCodes.append(int(key))
            UserArgs.append(value)
    
        def call(args):
            try:
                subprocess.check_call([f"{self.PyPath}", args])
                return 0
            except subprocess.CalledProcessError as e:
                return e.returncode

        while True:
            if ReturnValue is None:
                ClearScreen()
                ReturnValue = call(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{config.USER_CONFIGURATION['Launch']['ProjectMain']}")
                continue
            elif ReturnValue == 0: # Exit
                sys.exit(0)
            else: # Project Exit codes
                for code, arg in zip(UserCodes, UserArgs):
                    if code < 0:
                        code = 4294967296 + code # max value of 32-bit integer
                    if ReturnValue == code:
                        ClearScreen()
                        ReturnValue = call(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{config.USER_CONFIGURATION['Launch']['ProjectMain']} {arg}")
                        continue
            print("-----------------")
            print(f"It looks like something went wrong... Error: {ReturnValue}")
            print(f"Feel free to submit an issue at 'https://github.com/{config.USER_CONFIGURATION['Update']['Organization']}/{config.USER_CONFIGURATION['Update']['Repository']}/issues")
            if 'n' in input("Reload? (Y/n)"):
                sys.exit(0)
            ReturnValue = None

def ClearScreen():
    if "nt" in os.name:
        os.system("cls")
    else:
        os.system("clear")

def GetPython():
    path = os.environ['PATH'].split(";")
    for item in path:
        if item.endswith(os.sep):
            item = item[:-1]
        item = item.split(os.sep)
        if len(item) < 1:
            continue
        if item[-1] == config.USER_CONFIGURATION['Setup']['PythonFolder']:
            return(f"{os.sep}".join(item) + f"{os.sep}python.exe")
    return None

def old():
    if not os.path.exists("confpath.txt"):
        print("It looks like pyLaunch isn't configured. Please run 'start.py' to configure it.")
        input("Press enter to exit")
        sys.exit(0)
    with open("confpath.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        path = lines[0].strip()
        if os.name == "nt":
            path = path.replace("/", "\\")
        with open(path, "r", encoding="utf-8") as f:
            conf = json.load(f)

if __name__ == "__main__":
    print("This script is intended to be run from start.py")
    input("Press enter to exit")
    sys.exit(0)