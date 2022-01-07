
from .configuration import Configuration
from .serializer import Serialize

class CUI:
    def Launch(self):
        self.Configuration = Configuration()
        print("It looks like this project has no configuration!")
        print("If you're not the developer of this program, please\ntell them: 'pyLaunch has no configuration'\nTo use this program, launch it directly")
        print("\nDevelopers:")
        input("Press enter to continue")
        self._Configure()
        return True

    def _Configure(self):
        print("-------------------------")
        print("This program is broken into three categories, setup, update, and launch.")
        print("Setup:")
        print("\tRequired python version, required packages")
        print("Update:")
        print("\tGitHub details for update checking/downloading")
        print("Launch")
        print("\tProvides error catching, and python reloading")
        input("Press enter to begin configuring pyLaunch:Setup")
        self._ConfigureSetup()
        self._ConfigureUpdate()
        self._ConfigureLaunch()
        print("It looks like you're finished!")
        print("Lets save and reload just to be sure it works.")
        Serialize(self.Configuration.data)

    def _ConfigureSetup(self):
        print("\npyLaunch:Setup")
        print("------------------")
        while True:
            while True:
                PythonVersion = input("Required Python Version (ex: 3.10) > ")
                if len(PythonVersion.split(".")) <= 1:
                    if not 'y' in input(f"Are you sure you want Python {PythonVersion} (y/N) "):
                        continue
                self.Configuration['Setup']['PythonVersion'] = PythonVersion
                self.Configuration['Setup']['PythonFolder'] = "Python" + PythonVersion.replace(".", "")
                break
            while True:
                pypiName = []
                importName = []
                done = False
                print("Required python packages: ")
                while True:
                    print("\tAvailable commands: ")
                    print("\t -1) Finish")
                    print("\t  0) Help (print this page)")
                    print("\t  1) List")
                    print("\t  2) Remove")
                    print("---------------")
                    print("Please input a package as follows: pypiName:importName (ex: pyyaml:yaml)")
                    print("\tpypiName is the name you would use to install it through pip (pyyaml)")
                    print("\timportName is the name you would use to import it (yaml)")
                    print("\tif they are the same, simply provide: pypiName (ex:numpy)")
                    print("---------------")
                    while True:
                        package = input("Provide a package > ")
                        try:
                            package = int(package)
                            if package == -1:
                                print("Please verify the required packages:")
                                for idx, package in enumerate(pypiName):
                                    print(f"{package} : {importName[idx]}")
                                if 'y' in input("Is this correct? (y/N) > "):
                                    done = True
                                    for py, imp in zip(pypiName, importName):
                                        self.Configuration['Setup']['Packages'][py] = imp
                                    break
                            elif package == 0:
                                break
                            elif package == 1:
                                for idx, package in enumerate(pypiName):
                                    print(f"{idx + 1}) {package} : {importName[idx]}")
                            elif package == 2:
                                for idx, package in enumerate(pypiName):
                                    print(f"{idx + 1}) {package} : {importName[idx]}")
                                remove = input("Please specify which number to remove > ")
                                try:
                                    remove = int(remove)
                                    if remove - 1 < len(pypiName):
                                        pypiName.remove(remove)
                                        importName.remove(remove)
                                        break
                                    else:
                                        print("Please provide a valid number")
                                except ValueError:
                                    print("Please provide a number")
                        except ValueError:
                            if ":" in package:
                                package = package.split(":")
                                pypiName.append(package[0])
                                importName.append(package[1])
                            else:
                                pypiName.append(package)
                                importName.append(package)
                    if done:
                        break
                if done:
                    break
            return True

    def _ConfigureUpdate(self):
        print("\npyLaunch:Update")
        print("------------------")
        while True:
            Organization = input("Enter your github organization/username (ex: daavofficial) > ")
            Repository = input("Enter your github repository (ex: pyLaunch) > ")
            Branch = input("Enter your github branch (ex: main) > ")
            VersionPath = input("Enter your project version path (ex: /src/config/config.py) > ")
            Find = input("Enter the string to locate the version (ex: VERSION = ) > ")
            Token = input("Enter your GitHub token (only for private repositories) or press enter > ")
            if 'y' in input("Are these all correct? (y/N) > "):
                self.Configuration['Update']['Organization'] = Organization
                self.Configuration['Update']['Repository'] = Repository
                self.Configuration['Update']['Branch'] = Branch
                self.Configuration['Update']['VersionPath'] = VersionPath
                self.Configuration['Update']['Find'] = Find
                if Token == "": 
                    self.Configuration['Update']['Token'] = None
                else:
                    self.Configuration['Update']['Token'] = Token
                break
        return True

    def _ConfigureLaunch(self):
        print("\npyLaunch:Launch")
        print("------------------")
        while True:
            ProjectRoot = input("Please provide the relative path to your project from pyLaunch (ex: ..) > ")
            ProjectMain = input("Please provide the project path to your main script (ex /src/main.py) > ")
            self.Configuration['Launch']['ProjectRoot'] = ProjectRoot
            self.Configuration['Launch']['ProjectMain'] = ProjectMain
            print("Launch uses exit codes to preform specific functions, or provide error information")
            print("For the best results, use small negative numbers")
            errorCodes = []
            arguments = []
            done = False
            while True:
                print("\tAvailable commands: ")
                print("\t finish, f")
                print("\t help, h (print this page)")
                print("\t list, l")
                print("\t remove, r")
                print("Please input an error code as follows: ##:arguments")
                print("\t## is the number you want to use (ex: -2)")
                print("\targuments specifies the arguments to use (ex: -UI GUI)")
                print("\tproviding no arguments reloads python and launches your project (ex -1:)")
                while True:
                    code = input("Input an error code > ")
                    if code == "finish" or code == "f":
                        print("Please verify your exit codes:")
                        for idx, code in enumerate(errorCodes):
                            print(f"{code} : {arguments[idx]}")
                        if 'y' in input("Is this correct? (y/N) > "):
                            done = True
                            for code, arg in zip(errorCodes, arguments):
                                self.Configuration['Launch'][code] = arg
                            break
                    elif code == "help" or code == "h":
                        break
                    elif code == "list" or code == "l":
                        for idx, code in enumerate(errorCodes):
                            print(f"{idx + 1}) {code} : {arguments[idx]}")
                    elif code == "remove" or code == "r":
                        for idx, code in enumerate(errorCodes):
                            print(f"{idx + 1}) {code} : {arguments[idx]}")
                        remove = input("Please specify which number to remove > ")
                        try:
                            remove = int(remove)
                            if remove - 1 < len(errorCodes):
                                errorCodes.remove(remove)
                                arguments.remove(remove)
                                break
                            else:
                                print("Please provide a valid number")
                        except ValueError:
                            print("Please provide a number")
                    else:
                        code = code.split(":")
                        if len(code) <= 1 or len(code) > 2:
                            print("Invalid code, type 'help' to view formatting")
                        else:
                            errorCode = 0
                            try:
                                errorCode = int(code[0])
                            except ValueError:
                                print("You must provide an integer for the error code")
                                continue
                            if errorCode == -1:
                                print("-1 is reserved for updates")
                                continue
                            errorCodes.append(code[0])
                            arguments.append(code[1])
                if done:
                    break
            if done:
                break
        return True