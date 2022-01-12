import helpers.config as config

class Configuration:
    def __init__(self):
        self.data = dict(
            # -- DO NOT EDIT -- #
            Version = config.VERSION_CONFIGURATION,
            MinimumVersion = "1.0.1",
            # ----------------- #
            UI = "GUI",
            Setup = dict(
                PythonVersion = None, # ex: 3.10
                MinimumPythonVersion = None, # ex: 3.6
                Packages = {}, # pypiName : importName

                PythonFolder = None # "Python" + PythonVersion with the '.' removed
            ),
            Update = dict(
                Organization = None, # GitHub organization/user [ex: daavofficial]
                Repository = None, # Repository Name [ex: Project-Management]
                Branch = None, # Branch to check [ex: main]
                VersionPath = None, # project path to file containing version [ex: /src/config/config.py]
                Find = None, # line to grab for version [ex: VERSION = ]
                Token = False, # GitHub token for private repositories

                SkipCheck = False # if true: don't automatically check for updates
            ),
            Launch = dict(
                ProjectRoot = None, # Relative path to project root
                ProjectMain = None, # project path to the 'main' file
                ErrorCodes = {}, # code : arguments

                SkipCheck = False # if true, don't catch return codes (exit)
            ),
        )

    def __getitem__(self, key: str):
            return self.data.get(key, None)

    def __setitem__(self, key: str, value):
        self.data[key] = value