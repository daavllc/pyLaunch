import webbrowser
import os
import sys
import subprocess
import json

import helpers.config as config
from helpers.logger import Logger

from frontend.setup import Setup

class Launcher:
    __instance = None

    @staticmethod
    def Get():
        if Launcher.__instance is None:
            return Launcher()
        return Launcher.__instance

    def __init__(self):
        if Launcher.__instance is not None:
            return
        else:
            self.log = Logger("pyLaunch.Frontend.Launcher", "frontend.log")
            self.PyPath = None

    def Example(self):
        self.PyPath = GetPython()
        if self.PyPath is None:
            print(f"Uh oh, we couldn't find the required python version...")
            print(f"Please install Python {config.CONFIGURATION['Setup']['PythonVersion']} and try again")
            if 'y' in input("Open webrowser to download? (y/N) > "):
                webbrowser.open("https://www.python.org/downloads/")
            input("Press enter to exit")
            sys.exit(0)
        print(f"Using Python at: {self.PyPath}")

        # Run setup script and install required packages
        Setup(self.PyPath)
        self.Launch()

    def Initialize(self) -> bool:
        self.PyPath = GetPython()
        if self.PyPath is None:
            return False
        return True

    def Launch(self):
        ReturnValue = None
        UserCodes = []
        UserArgs = []
        for key, value in config.CONFIGURATION['Launch']['ErrorCodes'].items():
            UserCodes.append(int(key))
            UserArgs.append(value)
    
        def call(args: str = ""):
            try:
                if args == "":
                    subprocess.check_call([f"{self.PyPath}", f"{config.CONFIGURATION['Launch']['ProjectRoot']}{config.CONFIGURATION['Launch']['ProjectMain']}"])
                else:
                    command = [f"{self.PyPath}", f"{config.CONFIGURATION['Launch']['ProjectRoot']}{config.CONFIGURATION['Launch']['ProjectMain']}"]
                    args = args.split(" ")
                    for arg in args:
                        command.append(arg)
                    subprocess.check_call(command)
                return 0
            except subprocess.CalledProcessError as e:
                return e.returncode

        if config.CONFIGURATION['Launch']['SkipCheck']:
            call()
            sys.exit(0)

        while True:
            if ReturnValue is None:
                ClearScreen()
                ReturnValue = call()
                continue
            elif ReturnValue == 0: # Exit
                sys.exit(0)
            else: # Project Exit codes
                valid = False
                for code, arg in zip(UserCodes, UserArgs):
                    if code < 0:
                        code = 4294967296 + code # max value of 32-bit integer 4294967295
                    if ReturnValue == code:
                        ClearScreen()
                        ReturnValue = call(arg)
                        valid = True
                        break
                if valid:
                    continue
            print("-----------------")
            print(f"It looks like something went wrong... Error: {ReturnValue}")
            print(f"Feel free to submit an issue at https://github.com/{config.CONFIGURATION['Update']['Organization']}/{config.CONFIGURATION['Update']['Repository']}/issues")
            if 'n' in input("Reload? (Y/n) > "):
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
        if item[-1] == config.CONFIGURATION['Setup']['PythonFolder']:
            return(f"{os.sep}".join(item) + f"{os.sep}python.exe")
    return None

if __name__ == "__main__":
    print("This script is intended to be run from start.py")
    input("Press enter to exit")
    sys.exit(0)