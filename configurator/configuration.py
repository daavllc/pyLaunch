import config

class Configuration:
    def __init__(self):
        self.data = dict(
            Version = config.VERSION_CONFIGURATION,
            Setup = dict(
                PythonVersion = "", # ex: 3.10
                PythonFolder = "Python", # PythonVersion is appended with the '.' removed
                Packages = {} # Packages, pypiName : importName
            ),
            Update = dict(
                Organization = "", # GitHub organization/user
                Repository = "", # Repository Name
                Branch = "main",
                VersionPath = "", # project path to file containing version
                Find = "VERSION = ", # line to grab for version
                Token = None # GitHub token for private repositories
            ),
            Launch = dict(
                ProjectRoot = None, # Relative path to project root
                ProjectMain = None # project path to the 'main' file
            )
        )

    def __getitem__(self, key: str):
            return self.data.get(key, None)

    def __setitem__(self, key: str, value):
        self.data[key] = value