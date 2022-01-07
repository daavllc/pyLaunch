import webbrowser

import helpers.config as config

from user.update import Update
from user.launch import Launch
from user.setup import Setup

class CUI:
    def __init__(self):
        self.Status = [False, False, False]

    def Start(self):
        self.Automatic()

    def Automatic(self):
        self.InitUpdate()
        self.InitLaunch()
        self.InitSetup()
        if self.Status[0] and self.Status[1] and self.Status[2]:
            print("Launching!")
            self.Launch.pyLaunch()
        else:
            print("Unable to launch [", end="")
            print("Update: ", end="")
            if self.Status[0]:
                print("Success", end="")
            else:
                print("Failure", end="")
            print(", Launch: ", end="")
            if self.Status[1]:
                print("Success", end="")
            else:
                print("Failure", end="")
            print(", Setup: ", end="")
            if self.Status[2]:
                print("Success", end="")
            else:
                print("Failure", end="")
            print("]")
        return

    def InitUpdate(self):
        self.Update = Update()
        if not self.Update.CheckConnection():
            print("Unable to connect to the internet")
            self.Status[0] = True
            return
        print("Checking for update...")
        if self.Update.Check():
            print("An update is available")
            if not 'n' in input(f"Update from [v{'.'.join(self.Update.Versions[0])}] to [v{'.'.join(self.Update.Versions[1])}]? > ").lower():
                self.InstallUpdate()
            self.Status[0] = True
        else:
            print("You have the latest version")
            self.Status[0] = True

    def InstallUpdate(self):
        if not self.Update.DownloadUpdate():
            print("Failed to download update")
            self.Status[0] = True
        else:
            print("Downloaded")
        
        if not self.Update.InstallUpdate():
            print("Failed to install update")
            self.Status[0] = True
        self.Status[0] = True

    def InitLaunch(self):
        self.Launch = Launch()
        if not self.Launch.Initialize():
            print(f"Unable to locate Python {config.USER_CONFIGURATION['Setup']['PythonVersion']}")
            print(f"Please install Python {config.USER_CONFIGURATION['Setup']['PythonVersion']} and try again")
            if 'y' in input("Open webrowser to download? (y/N) > "):
                webbrowser.open("https://www.python.org/downloads/")
            input("Press enter to exit")
            exit(0)
        self.Status[1] = True

    def InitSetup(self):
        self.Setup = Setup(self.Launch.PyPath)
        self.MissingPackages = self.Setup.GetRequired()

        if len(self.MissingPackages) == 0:
            print("All required packages are installed")
            self.Status[2] = True
            return
        for package in self.MissingPackages:
            if 'n' in input(f"Package '{package[0]}' is not installed and required to use this program. Install? (Y/n): ").lower():
                return
            if not self.Setup.InstallPackage(package[0], package[1]):
                print(f"Failed to install {package[0]}")
                return
        self.Status[2] = True
