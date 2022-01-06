import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import shutil
from zipfile import ZipFile

import config

class Update:
    def __init__(self):
        self.DeleteFolders = ["src"]
        self.UpdateFolder = "updatefiles"

    def Automatic(self) -> bool:
        if not self.CheckConnection():
            return False
        UpdateAvailable = self.Check()
        if UpdateAvailable:
            print(f"An update is available! [v{'.'.join(self.Versions[1])}]")
            if not 'n' in input(f"Would you like to update from [{'.'.join(self.Versions[0])}]? (Y/n) > "):
                if self.DownloadUpdate():
                    return self.InstallUpdate()
        return False

    def CheckConnection(self) -> bool:
        try:
            urllib.request.urlopen('http://google.com')
            return True
        except Exception as e:
            return False # Unable to connect to the internet

    def DownloadUpdate(self) -> bool:
        response = None
        try:
            response = urllib.request.urlopen(f"https://api.github.com/repos/{config.USER_CONFIGURATION['Update']['Organization']}/{config.USER_CONFIGURATION['Update']['Repository']}/zipball/{config.USER_CONFIGURATION['Update']['Branch']}")
        except urllib.error.HTTPError as e:
            print(f"Unable to download update from GitHub: {e}")
            input("Press enter to continue...")
            return False

        if not os.path.exists(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{self.UpdateFolder}"):
            os.mkdir(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{self.UpdateFolder}")
        with open(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{self.UpdateFolder}{os.sep}gh_download.zip", "wb") as f:
            f.write(response.read())

        # Zip is downloaded, now extract
        zipFileContent = dict()
        zipFileContentSize = 0
        with ZipFile(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{self.UpdateFolder}{os.sep}gh_download.zip", 'r') as zipFile:
            for name in zipFile.namelist():
                zipFileContent[name] = zipFile.getinfo(name).file_size
            zipFileContentSize = sum(zipFileContent.values())
            extractedContentSize = 0
            for zippedFileName, zippedFileSize in zipFileContent.items():
                UnzippedFilePath = os.path.abspath(f"{zippedFileName}")
                os.makedirs(os.path.dirname(UnzippedFilePath), exist_ok=True)
                if os.path.isfile(UnzippedFilePath):
                    zipFileContentSize -= zippedFileSize
                else:
                    zipFile.extract(zippedFileName, path="", pwd=None)
                    extractedContentSize += zippedFileSize
                try:
                    done = int(50*extractedContentSize/zipFileContentSize)
                    percentage = (extractedContentSize / zipFileContentSize) * 100
                except ZeroDivisionError:
                    done = 50
                    percentage = 100
                sys.stdout.write('\r[{}{}] {:.2f}%'.format('█' * done, '.' * (50-done), percentage))
                sys.stdout.flush()
        sys.stdout.write('\n')
        return True

    def InstallUpdate(self) -> bool:
        print("Installing new version")
        newPath = None
        for file in os.listdir(config.USER_CONFIGURATION['Launch']['ProjectRoot']):
            if os.path.isdir(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{file}"):
                if file in self.DeleteFolders:
                    shutil.rmtree(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{file}")
                if file == self.UpdateFolder:
                    for item in os.listdir(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{file}"):
                        if os.path.isdir(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{file}{os.sep}{item}"):
                            newPath = f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{file}{os.sep}{item}"
            else: # Files
                os.remove(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{file}")

        # Old version is deleted

        for file in os.listdir(newPath):
            os.rename(f"{newPath}{os.sep}{file}", f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{file}")
        shutil.rmtree(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{self.UpdateFolder}")
        return True

    def Check(self) -> bool:
        self.Versions = self.GetVersions()
        self.Versions[0] = self.GetVersionAsInt(self.Versions[0])
        self.Versions[1] = self.GetVersionAsInt(self.Versions[1])
        self.Difference = []
        for installed, checked in zip(self.Versions[0], self.Versions[1]):
            self.Difference.append(checked - installed)
        
        for section in self.Difference:
            if section < 0: # When working on project and updating locally
                return False
            elif section > 0:
                return True
        return False

    def GetVersions(self) -> list:
        if not os.path.exists(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{config.USER_CONFIGURATION['Update']['VersionPath']}"):
            return None

        InstalledVersion = None
        CheckedVersion = None

        with open(f"{config.USER_CONFIGURATION['Launch']['ProjectRoot']}{os.sep}{config.USER_CONFIGURATION['Update']['VersionPath']}", "r") as f:
            lines = f.readlines()
            InstalledVersion = self.GetVersion(lines)

        try:
            response = urllib.request.urlopen(f"https://raw.githubusercontent.com/{config.USER_CONFIGURATION['Update']['Organization']}/{config.USER_CONFIGURATION['Update']['Repository']}/{config.USER_CONFIGURATION['Update']['Branch']}{config.USER_CONFIGURATION['Update']['VersionPath']}")
            content = response.read().decode("UTF-8").split("\n")
            CheckedVersion = self.GetVersion(content)
        except urllib.error.HTTPError as e:
            return False # URL doesn't exist or something went wrong

        return [InstalledVersion, CheckedVersion]

    def GetVersion(self, lines: str) -> str:
        for line in lines:
            line = line.strip()
            if config.USER_CONFIGURATION['Update']['Find'] in line:
                return line[len(config.USER_CONFIGURATION['Update']['Find']):].strip('"')

    def GetVersionAsInt(self, version: str) -> list:
        version = version.split(".")
        intVer = []
        for section in version:
            if section.isalnum():
                newSection = ""
                for char in section:
                    if char.isnumeric():
                        newSection += char
                section = newSection
            intVer.append(int(section))
        return intVer