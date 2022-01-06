import sys
import subprocess
import importlib.util

import config

class Setup:
    def __init__(self, PyPath: str):
        self.PyPath = PyPath
        self.Required = []
        self.CheckedPip = False

    def Automatic(self):
        for pypi, imp in config.USER_CONFIGURATION['Setup']['Packages'].items():
            if not self.AutoValidatePackage(pypi, imp):
                print(f"Unable to validate package '{pypi}'")

    def GetRequired(self) -> list:
        for pypi, imp in config.USER_CONFIGURATION['Setup']['Packages'].items():
            if not self.ValidatePackage(pypi, imp):
                self.Required.append([pypi, imp])
        return self.Required

    def ValidatePackage(self, pypi, imp) -> bool:
        if (importlib.util.find_spec(pypi)) is not None:
            return True
        else:
            try: # Attempt to import package by name
                __import__(imp)
                return True
            except ImportError as e:
                pass
        return False

    def InstallPackage(self, pypi, imp) -> bool:
        subprocess.check_call([f"{self.PyPath}", "-m", "pip", "install", pypi])
        return self.ValidatePackage(pypi, imp)

    def AutoValidatePackage(self, pypi, imp):
        if (importlib.util.find_spec(pypi)) is not None:
            return True
        else:
            try: # Attempt to import package by name
                __import__(imp)
                return True
            except ImportError as e:
                pass
        return self.AutoInstallPackage(pypi, imp)

    def AutoInstallPackage(self, pypi, imp):
        self.UpdatePip()
        if 'n' in input(f"Package '{pypi}' is not installed and required to use this program. Install '{pypi}'? (Y/n): ").lower():
            return False

        print(f"Installing {pypi}...")
        subprocess.check_call([f"{self.PyPath}", "-m", "pip", "install", pypi])

        return self.ValidatePackage(pypi, imp)

    def UpdatePip(self):
        if self.CheckedPip:
            return
        subprocess.check_call([f"{self.PyPath}", "-m", "pip", "install", "-U", "pip"])
        self.CheckedPip = True