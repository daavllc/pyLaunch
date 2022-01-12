import requests
import urllib

from .cui import CUI
from .gui import GUI
from .serializer import Serialize, Deserialize
from .configuration import Configuration

class Configurator:
    __instance = None

    @staticmethod
    def Get():
        if Configurator.__instance is None:
            return Configurator()
        return Configurator.__instance

    def __init__(self):
        if Configurator.__instance is not None:
            return
        else:
            self.Configuration = Configuration()
            self.Update = self._Update(self)
            self.Setup = self._Setup(self)
            self.Launch = self._Launch(self)

    def New(self, UI: str) -> bool:
        """ pyLaunch has not been configured, so let's configure it """
        if UI == "GUI":
            self.UI = GUI(self)
        else:
            self.UI = CUI(self)
        return self.UI.Launch() # This uses the specified UI, creates the configuration, and serializes it
        

    def Load(self) -> None:
        """ pyLaunch is configured, load that configuration and execute """
        self.Configuration.data = Deserialize()

    def Save(self) -> None:
        Serialize(self.Configuration.data)
    class _Setup:
        def __init__(self, parent):
            self.parent = parent
            self.keys = [key for key in self.parent.Configuration['Setup'].keys()]

        def Set(self, pythonVersion: str, minimumPythonVersion: str, Packages: dict) -> list:
            success = []
            success.append(self.SetPythonVersion(pythonVersion))
            success.append(self.SetMinimumPythonVersion(minimumPythonVersion))
            success.append(self.SetPackages(Packages))
            return success

        def SetPythonVersion(self, pythonVersion: str) -> str:
            if pythonVersion == "":
                return "No Python Version provided"
            if not "." in pythonVersion or len(pythonVersion) > 8:
                return "Invalid Python version"
            self.parent.Configuration['Setup']['PythonVersion'] = pythonVersion
            self.parent.Configuration['Setup']['PythonFolder'] = "Python" + pythonVersion.replace(".", "")
            return None

        def SetMinimumPythonVersion(self, minimumPythonVersion: str) -> str:
            if minimumPythonVersion == "":
                self.parent.Configuration['Setup']['MinimumPythonVersion'] = self.parent.Configuration['Setup']['PythonVersion']
            else:
                if not "." in minimumPythonVersion or len(minimumPythonVersion) > 8:
                    return "Invalid minimum Python version"
                self.parent.Configuration['Setup']['MinimumPythonVersion'] = minimumPythonVersion
            return None

        def SetPackages(self, packages: dict) -> str:
            self.parent.Configuration['Setup']['Packages'] = packages
            return None

    class _Update:
        def __init__(self, parent):
            self.parent = parent
            self.keys = [key for key in self.parent.Configuration['Update'].keys()]

        def Set(self, org: str, repo: str, branch: str, versionPath: str, find: str, token: str, skipCheck: bool) -> list:
            success = []
            try:
                urllib.request.urlopen('http://google.com')
            except Exception as e:
                return None # no internet connection
            skip = False
            if token:
                if self._Verify(f"http://www.github.com/{org}/{repo}/tree/{branch}{versionPath}", headers={'authorization':token}):
                    return True
            else:
                if self._Verify(f"http://www.github.com/{org}/{repo}/tree/{branch}{versionPath}"):
                    skip = True
            success.append(self.SetToken(token))
            success.append(self.SetOrganization(org, skip))
            success.append(self.SetRepository(repo, skip))
            success.append(self.SetBranch(branch, skip))
            success.append(self.SetVersionPath(versionPath, skip))
            success.append(self.SetFind(find))
            success.append(self.SetSkipCheck(skipCheck))
            return success

        def _Verify(self, url, headers: dict = None):
            response = None
            if headers is None:
                response = requests.get(url)
            else:
                response = requests.get(url, headers)
            if response.status_code == 200:
                return True
            return False

        def SetOrganization(self, org: str, skip = False) -> str:
            if org == "":
                return "No organization provided"
            if not skip:
                response = requests.get(f"http://www.github.com/{org}")
                if response.status_code == 200:
                    self.parent.Configuration['Update']['Organization'] = org
                    return None
                return "Organization does not exist"
            self.parent.Configuration['Update']['Organization'] = org
            return None

        def SetRepository(self, repo: str, skip = False) -> str:
            if repo == "":
                return "No repository provided"
            if not skip:
                if self.parent.Configuration['Update']['Organization'] is None:
                    return "Organization is not configured"
                response = None
                if self.parent.Configuration['Update']['Token'] is None:
                    response = requests.get(f"http://www.github.com/{self.parent.Configuration['Update']['Organization']}/{repo}")
                else:
                    response = requests.get(f"http://www.github.com/{self.parent.Configuration['Update']['Organization']}/{repo}", headers={'authorization':self.parent.Configuration['Update']['Token']})
                if response.status_code == 200:
                    self.parent.Configuration['Update']['Repository'] = repo
                    return None
                return "Repository does not exist"
            self.parent.Configuration['Update']['Repository'] = repo
            return None

        def SetBranch(self, branch: str, skip = False) -> str:
            if branch == "":
                return "No branch provided"
            if not skip:
                if self.parent.Configuration['Update']['Organization'] is None:
                    return "Organization is not configured"
                elif self.parent.Configuration['Update']['Repository'] is None:
                    return "Repository is not set"
                response = requests.get(f"http://www.github.com/{self.parent.Configuration['Update']['Organization']}/{self.parent.Configuration['Update']['Repository']}/tree/{branch}")
                if response.status_code == 200:
                    self.parent.Configuration['Update']['Branch'] = branch
                    return None
                return "Branch does not exist"
            self.parent.Configuration['Update']['Branch'] = branch
            return None

        def SetVersionPath(self, versionPath: str, skip = False) -> str:
            if versionPath == "":
                return "No Version Path provided"
            if not skip:
                if self.parent.Configuration['Update']['Organization'] is None:
                    return "Organization is not configured"
                elif self.parent.Configuration['Update']['Repository'] is None:
                    return "Repository is not configured"
                elif self.parent.Configuration['Update']['Branch'] is None:
                    return "Branch is not configured"
                response = requests.get(f"http://www.github.com/{self.parent.Configuration['Update']['Organization']}/{self.parent.Configuration['Update']['Repository']}/tree/{self.parent.Configuration['Update']['Branch']}{versionPath}")
                if response.status_code == 200:
                    self.parent.Configuration['Update']['VersionPath'] = versionPath
                    return None
                return "Path does not exist"
            self.parent.Configuration['Update']['VersionPath'] = versionPath
            return None

        def SetFind(self, find: str) -> str:
            if find == "":
                return "No find string provided"
            self.parent.Configuration['Update']['Find'] = find
            return None

        def SetToken(self, token: str) -> str:
            if token:
                self.parent.Configuration['Update']['Token'] = token
            else:
                self.parent.Configuration['Update']['Token'] = None
            return None

        def SetSkipCheck(self, skipCheck: bool) -> str:
            self.parent.Configuration['Update']['SkipCheck'] = skipCheck
            return None

    class _Launch:
        def __init__(self, parent):
            self.parent = parent
            self.keys = [key for key in self.parent.Configuration['Launch'].keys()]

        def Set(self, projectRoot: str, projectMain: str, errorCodes: dict, skipCheck: bool) -> list:
            success = []
            success.append(self.SetProjectRoot(projectRoot))
            success.append(self.SetProjectMain(projectMain))
            success.append(self.SetErrorCodes(errorCodes))
            success.append(self.SetSkipCheck(skipCheck))
            return success

        def SetProjectRoot(self, projectRoot: str) -> str:
            if projectRoot == "":
                return "No Project Root provided"
            self.parent.Configuration['Launch']['ProjectRoot'] = projectRoot
            return None

        def SetProjectMain(self, projectMain: str) -> str:
            if projectMain == "":
                return "No Project Main provided"
            self.parent.Configuration['Launch']['ProjectMain'] = projectMain
            return None

        def SetErrorCodes(self, errorCodes: dict) -> str:
            self.parent.Configuration['Launch']['ErrorCodes'] = errorCodes
            return None

        def SetSkipCheck(self, skipCheck: bool) -> str:
            self.parent.Configuration['Launch']['SkipCheck'] = skipCheck
            return None