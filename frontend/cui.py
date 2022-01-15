import webbrowser

import helpers.config as config

from frontend.update import Updater
from frontend.launch import Launcher
from frontend.setup import Setup

class CUI:
    def __init__(self):
        self.Status = [False, False, False]

    def Start(self):
        self.Automatic()

    def Automatic(self):
        if self.InitUpdate():
            if self.InitLaunch():
                self.InitSetup()
        if self.Status[0] and self.Status[1] and self.Status[2]:
            print("Launching!")
            self.Launch.Launch()
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
            input("Press enter to exit")
        return

    def InitUpdate(self):
        self.Update = Updater()
        status = self.Update.CheckConnection()
        if type(status) == str:
            print(status)
            self.Status[0] = True
            return True
        print("Checking for update...")
        status = self.Update.CheckVersions()
        if type(status) == list:
            if status[1]: # Can still continue
                print(status[0])
                self.Status[0] = True
                return True
            else:
                print(f"Error {status[0]}")
                return False
        elif status:
            print("An update is available")
            if not 'n' in input(f"Update from [v{'.'.join([str(sec) for sec in self.Update.Versions[0]])}] to [v{'.'.join([str(sec) for sec in self.Update.Versions[1]])}]? (Y/n) > ").lower():
                self.InstallUpdate()
            self.Status[0] = True
            return True
        else:
            print("You have the latest version")
            self.Status[0] = True
            return True

    def InstallUpdate(self):
        if not self.Update.DownloadUpdate():
            print("Failed to download update")
            self.Status[0] = True
            return True
        else:
            print("Downloaded")
        
        if not self.Update.InstallUpdate():
            print("Failed to install update")
            self.Status[0] = False
            return False
        self.Status[0] = True
        return True

    def InitLaunch(self):
        self.Launch = Launcher()
        if not self.Launch.Initialize():
            print(f"Unable to locate Python {config.CONFIGURATION['Setup']['PythonVersion']}")
            print(f"Please install Python {config.CONFIGURATION['Setup']['PythonVersion']} and try again")
            if 'y' in input("Open webrowser to download? (y/N) > "):
                webbrowser.open("https://www.python.org/downloads/")
            return False
        self.Status[1] = True
        return True

    def InitSetup(self):
        self.Setup = Setup(self.Launch.PyPath)
        self.MissingPackages = self.Setup.GetRequired()

        if len(self.MissingPackages) == 0:
            print("All required packages are installed")
            self.Status[2] = True
            return True
        for package in self.MissingPackages:
            if 'n' in input(f"Package '{package[0]}' is not installed and required to use this program. Install? (Y/n): ").lower():
                return False
            if not self.Setup.InstallPackage(package[0], package[1]):
                print(f"Failed to install {package[0]}")
                return False
        self.Status[2] = True
