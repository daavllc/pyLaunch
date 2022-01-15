
import helpers.config as config
class CUI:
    def __init__(self, configurator):
        self.Configurator = configurator
    class Storage:
        pass
    def Launch(self):
        print("It looks like this project has no configuration!")
        print("If you're not the developer of this program, please\ntell them: 'pyLaunch has no configuration'\nTo use this program, launch it directly")
        print("\nDevelopers:")
        input("Press enter to continue")
        self._Configure()
        return True

    def _Configure(self):
        print("-------------------------")
        print("Configuration is broken into three parts: updater, setup, and launcher.")
        print("Setup:")
        print("\tRequired python version, required packages")
        print("Update:")
        print("\tGitHub details for update checking/downloading")
        print("Launch")
        print("\tProvides error catching, and python reloading")
        print(f"Additional documentation can be found at {config.LINK_DOCUMENTATION}")
        input("Press enter to begin configuring pyLaunch:Updater")
        self._ConfigureUpdate()
        self._ConfigureSetup()
        self._ConfigureLaunch()
        print("It looks like you're finished!")
        print("Lets save and reload just to be sure it works.")
        self.Configurator.Save()

    def _ConfigureUpdate(self):
        print("\npyLaunch:Updater")
        print("------------------")
        while True:
            print("Enter your GitHub organization/username (ex: daavofficial)")
            Organization = input(" > ")
            print("Enter your github repository (ex: pyLaunch)")
            Repository = input(" > ")
            print("Enter your github branch (ex: main)")
            Branch = input(" > ")
            print("Enter your project version path (ex: /src/config/config.py)")
            VersionPath = input(" > ")
            print("Enter the string to locate the version (ex: VERSION = )")
            Find = input(" > ")
            print("Enter your GitHub token (only for private repositories) or press enter")
            Token = input(" > ")
            print("Skip checking for updates (press enter for no)")
            SkipCheck = input(" > ").lower()
            if SkipCheck:
                SkipCheck = True
            else:
                SkipCheck = False
            if 'n' in input("Are these all correct? (Y/n) > "):
                continue
            status = self.Configurator.Update.Set(Organization, Repository, Branch, VersionPath, Find, Token, SkipCheck)
            if all(element == None for element in status):
                print("Set successfully!")
                break
            else:
                for stat in status:
                    if stat is not None:
                        print(stat)
        return True

    def _ConfigureSetup(self):
        data = self.Storage()
        print("\npyLaunch:Setup")
        print("------------------")
        data.SkipCheck = False
        while True:
            while True:
                print("Enter your project's python version [ex: 3.10]")
                data.PythonVersion = input(" > ")
                print("Enter your projet's minimum Python version (leave blank for same as above)")
                data.MinimumPythonVersion = input(" > ")
                if 'n' in input("Are these correct? (Y/n) > "):
                    continue
                break
            while True:
                data.packages = {}
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
                                for key, value in data.packages.items():
                                    print(f"{key} : {value}")
                                if 'y' in input("Is this correct? (y/N) > "):
                                    status = self.Configurator.Setup.Set(data.PythonVersion, data.MinimumPythonVersion, data.packages)
                                    if all(element == None for element in status):
                                        done = True
                                        print("Set successfully!")
                                        break
                                    else:
                                        for stat in status:
                                            if stat is not None:
                                                print(stat)
                            elif package == 0:
                                break
                            elif package == 1:
                                index = 1
                                for key, value in data.packages.items():
                                    print(f"{index}) {key} : {value}")
                                    index += 1
                            elif package == 2:
                                index = 0
                                for key, value in data.packages.items():
                                    print(f"{key} : {value}")
                                    index += 1
                                remove = input("Please specify which package to remove > ")
                                if data.packages.get(remove, None) is not None:
                                    del data.packages[remove]
                                else:
                                    print("Please provide a valid package")
                        except ValueError:
                            if ":" in package:
                                package = package.split(":")
                                data.packages[package[0]] = package[1]
                            else:
                                data.packages[package] = package
                    if done:
                        break
                if done:
                    break
            return True

    def _ConfigureLaunch(self):
        print("\npyLaunch:Launcher")
        print("------------------")
        data = self.Storage()
        while True:
            print("Please provide the relative path to your project from pyLaunch (ex: ..)")
            data.ProjectRoot = input(" > ")
            print("Please provide the project path to your main script (ex /src/main.py)")
            data.ProjectMain = input(" > ")
            print("Skip checking return codes on exit? (press enter for no)")
            data.SkipCheck = input(" > ")
            if data.SkipCheck:
                data.SkipCheck = True
            else:
                data.SkipCheck = False
            print("Launcher uses exit codes to preform specific functions, or provide error information")
            print("For the best results, use small negative numbers")
            data.codes = {}
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
                        for key, value in data.codes.items():
                            print(f"{key} : {value}")
                        if 'y' in input("Is this correct? (y/N) > "):
                            done = True
                            status = self.Configurator.Launch.Set(data.ProjectRoot, data.ProjectMain, data.codes, data.SkipCheck)
                            if all(element == None for element in status):
                                print("Set successfully!")
                                break
                            else:
                                for stat in status:
                                    if stat is not None:
                                        print(stat)
                    elif code == "help" or code == "h":
                        break
                    elif code == "list" or code == "l":
                        for key, value in data.codes.items():
                            print(f"{key} : {value}")
                    elif code == "remove" or code == "r":
                        for key, value in data.codes.items():
                            print(f" {key} : {value}")
                        remove = input("Please specify which code to remove > ")
                        if data.codes.get(remove, None) is not None:
                            del data.codes[remove]
                        else:
                            print("Please provide a valid code")
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
                            data.codes[code[0]] = code[1]
                if done:
                    break
            if done:
                break
        return True