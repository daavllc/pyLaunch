
import tkinter as tk
from tkinter import ttk
import webbrowser

from .configuration import Configuration
from .serializer import Serialize
import config
from colors import Colors
c = Colors.Get()

class GUI:
    class Storage:
        pass
    def Launch(self):
        self.Initialize()
        self.Runtime()
        return self.Completed

    def Reset(self):
        self.ws = tk.Tk()

        self.Completed = False
        self.Configuration = Configuration()
        self.ConfigStatus = [False, False, False]
        self.Configuring = False
    
        self.data = self.Storage()
        self.Frames = self.Storage()
        self.Menus = self.Storage()

    def DarkMode(self):
        c.Set('dark')
        self.ws.destroy()
        self.Initialize()

    def LightMode(self):
        c.Set('light')
        self.ws.destroy()
        self.Initialize()

    def Initialize(self):
        self.Reset()
        self.ws.title(f"Launcher Configurator {config.VERSION}")
        self.ws.geometry("700x400")
        self.ws.resizable(width=False, height=False)

        # Menu
        self.Menus.Main = tk.Menu(self.ws)
        self.ws.config(menu=self.Menus.Main)

        # View
        self.Menus.View = tk.Menu(self.Menus.Main, tearoff=0, background=c.FRAME_BG1, foreground=c.LABEL_FG)
        self.Menus.Main.add_cascade(label="View", menu=self.Menus.View)

        self.Menus.View.add_command(label="Dark mode", command=self.DarkMode)
        self.Menus.View.add_command(label="Light mode", command=self.LightMode)

        # Help
        self.Menus.Help = tk.Menu(self.Menus.Main, tearoff=0, background=c.FRAME_BG1, foreground=c.LABEL_FG)
        self.Menus.Main.add_cascade(label="Help", menu=self.Menus.Help)

        self.Menus.Help.add_command(label="What's this?", command=self.PopupStartup)
        self.Menus.Help.add_separator()
        self.Menus.Help.add_command(label="About", command=self.PopupAbout)
        self.Menus.Help.add_separator()
        self.Menus.Help.add_command(label="Configuration", command=self.PopupConfiguration)
        self.Menus.Help.add_command(label="Setup", command=self.PopupSetup)
        self.Menus.Help.add_command(label="Update", command=self.PopupUpdate)
        self.Menus.Help.add_command(label="Launch", command=self.PopupLaunch)

        ######## Frames
        # Configuration
        self.Frames.Configuration = tk.Frame(self.ws, width=200, height=400, borderwidth=10, background=c.FRAME_BG2)
        self.Frames.Configuration.grid_propagate(0)
        self.Frames.Configuration.pack(fill='both', side='left', expand='False')
        ttk.Label(self.Frames.Configuration, text="Configurations", font=18, background=c.FRAME_BG2, foreground=c.LABEL_FG).grid(column=0, row=0)

        tk.Button(self.Frames.Configuration,  text="Setup",  command=self.ConfigureSetup, background=c.FRAME_BG2, foreground=c.LABEL_FG).grid(column=0, row=1)
        self.fr_cft_setup_status = ttk.Label(self.Frames.Configuration, text="Not complete", background=c.FRAME_BG2, foreground=c.LABEL_FG)
        self.fr_cft_setup_status.grid(column=1, row=1)
        tk.Button(self.Frames.Configuration, text="Update", command=self.ConfigureUpdate, background=c.FRAME_BG2, foreground=c.LABEL_FG).grid(column=0, row=2)
        self.fr_cft_update_status = ttk.Label(self.Frames.Configuration, text="Not complete", background=c.FRAME_BG2, foreground=c.LABEL_FG)
        self.fr_cft_update_status.grid(column=1, row=2)
        tk.Button(self.Frames.Configuration, text="Launch", command=self.ConfigureLaunch, background=c.FRAME_BG2, foreground=c.LABEL_FG).grid(column=0, row=3)
        self.fr_cft_launch_status = ttk.Label(self.Frames.Configuration, text="Not complete", background=c.FRAME_BG2, foreground=c.LABEL_FG)
        self.fr_cft_launch_status.grid(column=1, row=3)

        self.fr_cft_finish_label = ttk.Label(self.Frames.Configuration, text="", font=18, background=c.FRAME_BG2, foreground=c.LABEL_FG)
        self.fr_cft_finish_label.grid(column=0, row=4)
        tk.Button(self.Frames.Configuration, text="Finish", command=self.FinishConfiguration, background=c.FRAME_BG2, foreground=c.LABEL_FG).grid(column=0, row=5)

        # Configurator
        self.Frames.Configurator = tk.Frame(self.ws, width=500, height=400, borderwidth=10, background=c.FRAME_BG1)
        self.Frames.Configurator.grid_propagate(0)
        self.Frames.Configurator.pack(fill='both', side='right', expand='True')
        self.fr_cfr_title = tk.Label(self.Frames.Configurator, text="Select a configuration on the left", font=18, background=c.FRAME_BG1, foreground=c.LABEL_FG)
        self.fr_cfr_title.grid(column=0, row=0)
        self.fr_cfr_popup_btn = tk.Button(self.Frames.Configurator, text="What's this?", command=self.PopupStartup, background=c.FRAME_BG1, foreground=c.LABEL_FG)
        self.fr_cfr_popup_btn.grid(sticky="e", column=1, row=0, padx=50)
        self.Frames.CGR = tk.Frame(self.Frames.Configurator, width=500, height=350, borderwidth=10, background=c.FRAME_BG2)
        self.Frames.CGR.grid_propagate(0)
        self.Frames.CGR.pack(fill='both', side='bottom', expand='False')

    def PopupStartup(self):
        popup = tk.Toplevel(self.ws, background=c.FRAME_BG1)
        popup.geometry("350x225")
        popup.title("No valid configuration")
        popup.resizable(width=False, height=False)
        tk.Label(popup, text="It looks like this project has no configuration!", font=18, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="If you're not the developer of this program, please\ntell them: 'Launcher has no configuration'\nTo use this program, launch it directly", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Developers:", font=18, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Please set up each configuration on the left, then press finish", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="If you need any assistance, check the 'help' menu for\ninformation or check our GitHub page", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Button(popup, text="GitHub Page", command=lambda: webbrowser.open("https://github.com/daavofficial/Launcher"), background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Button(popup, text="Close", command=popup.destroy, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack(side='bottom')
    
    def PopupAbout(self):
        popup = tk.Toplevel(self.ws, background=c.FRAME_BG1)
        popup.geometry("250x200")
        popup.title("About")
        popup.resizable(width=False, height=False)
        tk.Label(popup, text=f"Launcher v{config.VERSION}", font=18, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text=f"©2022 DAAV, LLC", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text=f"Python project setup, updater, and launcher", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text=f"License: MIT", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Button(popup, text="Source Code", command=lambda: webbrowser.open("https://github.com/daavofficial/Launcher"), background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text=f"GUI v{config.VERSION_GUI}", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text=f"Project Launch v{config.VERSION_PROJECT_LAUNCH}", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text=f"Project Setup v{config.VERSION_PROJECT_SETUP}", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text=f"Project Update v{config.VERSION_PROJECT_UPDATE}", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()

    def PopupConfiguration(self):
        popup = tk.Toplevel(self.ws, background=c.FRAME_BG1)
        popup.geometry("350x100")
        popup.title("Help - Configuration")
        popup.resizable(width=False, height=False)
        tk.Label(popup, text="Configuration is broken into 3 parts:", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Button(popup, text="Setup: Required python version, required packages", command=self.PopupSetup, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Button(popup, text="Update: GitHub details for update checking/downloading", command=self.PopupUpdate, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Button(popup, text="Launch: Provides error catching, and python reloading", command=self.PopupLaunch, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()

    def PopupSetup(self):
        popup = tk.Toplevel(self.ws, background=c.FRAME_BG1)
        popup.geometry("400x300")
        popup.title("Help - Launcher:Setup")
        popup.resizable(width=False, height=False)
        tk.Label(popup, text="Setup simplifies installation by automatically", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="running python using your project's required version,", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="and will install all required packages automatically", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Setup requires two things:", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="The version on python your project uses", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="The packages your project depends on", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Python Version", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Simply provide the python version (ex: 3.10)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Required packages:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Packages contain two values: the pip install name, and the import name", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="If they are the same, just type the package name (ex: numpy)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="If they are different, delimit them with a colon (ex: pyyaml:yaml)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()

    def PopupUpdate(self):
        popup = tk.Toplevel(self.ws, background=c.FRAME_BG1)
        popup.geometry("400x320")
        popup.title("Help - Launcher:Update")
        popup.resizable(width=False, height=False)
        tk.Label(popup, text="Check installed version vs most recent version on GitHub", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Organization:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Your GitHub username (ex: daavofficial)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Repository:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Your GitHub repository's name (ex: Launcher)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Branch:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Branch to check (ex: main)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Version Path:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Repository path to the file that contains the version", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="(ex: /src/config.py)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Find:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="The string to look for to find the version (ex: VERSION = )", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Token:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Only needed for accessing private repositores", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()

    def PopupLaunch(self):
        popup = tk.Toplevel(self.ws, background=c.FRAME_BG1)
        popup.geometry("400x200")
        popup.title("Help - Launcher:Launch")
        popup.resizable(width=False, height=False)
        tk.Label(popup, text="Launch project and check error codes", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Project Root:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Relative path from Launcher to your Project's root folder", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Project Main:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Repository path to your project's main file (ex: /start.py)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Error Codes:", font=12, background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Error Codes contain two values: the code, and addional arguments", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="Error codes are formated as follows: 'code:args' (ex: -2:-UI GUI)", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()
        tk.Label(popup, text="If you provide and error code with no arguments, it will reload python", background=c.FRAME_BG1, foreground=c.LABEL_FG).pack()

    def Runtime(self):
        self.ws.mainloop()

    def FinishConfiguration(self):
        if not(self.ConfigStatus[0] and self.ConfigStatus[1] and self.ConfigStatus[2]):
            self.fr_cft_finish_label.config(text="Incomplete")
        else:
            self.fr_cft_finish_label.config(text="Done!")
            Serialize(self.Configuration.data)
            self.Completed = True
            self.ws.destroy()
            return True

    def UpdateStatus(self):
        if self.ConfigStatus[0]:
            self.fr_cft_setup_status.config(text="Done")
        else:
            self.fr_cft_setup_status.config(text="Not complete")
        if self.ConfigStatus[1]:
            self.fr_cft_update_status.config(text="Done")
        else:
            self.fr_cft_update_status.config(text="Not complete")
        if self.ConfigStatus[2]:
            self.fr_cft_launch_status.config(text="Done")
        else:
            self.fr_cft_launch_status.config(text="Not complete")

    def ClearConfigure(self):
        self.fr_cfr_title.config(text="Select a configuration on the left")
        for item in self.Frames.CGR.winfo_children():
            item.destroy()
        if self.fr_cfr_popup_btn is not None:
            self.fr_cfr_popup_btn.destroy()
            self.fr_cfr_popup_btn = None

    def ConfigureSetup(self):
        self.ClearConfigure()
        self.Configuring = True
        self.data.pypiName = []
        self.data.importName = []
        self.data.packagelist = []

        self.fr_cfr_title.config(text="Setup Configuration", background=c.FRAME_BG1, foreground=c.LABEL_FG)

        self.Frames.CGR_PythonVersion = tk.Frame(self.Frames.CGR, background=c.FRAME_BG1)
        self.Frames.CGR_PythonVersion.grid(sticky='w', column=0, row=0, pady=5)
        tk.Label(self.Frames.CGR_PythonVersion, justify="left", anchor="w", text="Required Python Version:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=0, padx=5)
        self.data.PythonVersion = tk.Text(self.Frames.CGR_PythonVersion, width=5, height=1)
        self.data.PythonVersion.grid(sticky='w', column=1, row=0)
        
        self.Frames.CGR_Packages = tk.Frame(self.Frames.CGR, background=c.FRAME_BG1)
        self.Frames.CGR_Packages.grid(sticky='w', column=0, row=1, pady=5)
        tk.Label(self.Frames.CGR_Packages, justify="left", anchor="w", text="Packages:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=0)
        tk.Label(self.Frames.CGR_Packages, width=10, text="pypiName", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(column=2, row=0)
        tk.Label(self.Frames.CGR_Packages, width=10, text="importName", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(column=3, row=0)
        tk.Button(self.Frames.CGR_Packages, text="Remove", command=self.RemovePackage, background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(column=4, row=0)
        self.data.PackageName = tk.Text(self.Frames.CGR_Packages, width=20, height=1)
        self.data.PackageName.grid(sticky='w', column=0, row=1, padx=5)
        tk.Button(self.Frames.CGR_Packages, text="Add", command=self.AddPackage, background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(column=1, row=1)

        tk.Button(self.Frames.CGR, text="Finish", command=self.SetSetup, background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(stick='s', pady=20)

    def DrawPackageList(self):
        for row in self.data.packagelist:
            for item in row:
                item.destroy()
        self.data.packagelist = []
        index = 0
        for py, imp in zip(self.data.pypiName, self.data.importName):
            pyNameLabel = tk.Label(self.Frames.CGR_Packages, justify="left", anchor="w", text=py, background=c.FRAME_BG1, foreground=c.LABEL_FG)
            pyNameLabel.grid(sticky='w', column=2, row=index + 1)
            importNameLabel = tk.Label(self.Frames.CGR_Packages, justify="left", anchor="w", text=imp, background=c.FRAME_BG1, foreground=c.LABEL_FG)
            importNameLabel.grid(sticky='w', column=3, row=index + 1)
            self.data.packagelist.append([pyNameLabel, importNameLabel])
            index += 1

    def AddPackage(self):
        package = self.data.PackageName.get("1.0", "end-1c")
        if ":" in package:
            package = package.split(":")
            self.data.pypiName.append(package[0])
            self.data.importName.append(package[1])
        else:
            self.data.pypiName.append(package)
            self.data.importName.append(package)
        self.DrawPackageList()

    def RemovePackage(self):
        if len(self.data.pypiName) == 0:
            return
        self.data.pypiName.pop()
        self.data.importName.pop()
        self.DrawPackageList()

    def SetSetup(self):
        self.Configuration['Setup']['PythonVersion'] = self.data.PythonVersion.get("1.0", "end-1c")
        self.Configuration['Setup']['PythonFolder'] = "Python" + self.Configuration['Setup']['PythonVersion'].replace(".", "")
        for py, imp in zip(self.data.pypiName, self.data.importName):
            self.Configuration['Setup']['Packages'][py] = imp
        self.data = self.Storage()
        self.ConfigStatus[0] = True
        self.UpdateStatus()
        print(str(self.Configuration.data['Setup']))

    def ConfigureUpdate(self):
        self.ClearConfigure()
        self.Configuring = True
        self.fr_cfr_title.config(text="Update Configuration")
        
        tk.Label(self.Frames.CGR, justify="left", anchor="w", text="Organization:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=0)
        self.data.Organization = tk.Text(self.Frames.CGR, width=40, height=1)
        self.data.Organization.grid(sticky='w', column=1, row=0, pady=5)

        tk.Label(self.Frames.CGR, justify="left", anchor="w", text="Repository:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=1)
        self.data.Repository = tk.Text(self.Frames.CGR, width=40, height=1)
        self.data.Repository.grid(sticky='w', column=1, row=1, pady=5)

        tk.Label(self.Frames.CGR, justify="left", anchor="w", text="Branch:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=2)
        self.data.Branch = tk.Text(self.Frames.CGR, width=40, height=1)
        self.data.Branch.grid(sticky='w', column=1, row=2, pady=5)

        tk.Label(self.Frames.CGR, justify="left", anchor="w", text="VersionPath:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=3)
        self.data.VersionPath = tk.Text(self.Frames.CGR, width=40, height=1)
        self.data.VersionPath.grid(sticky='w', column=1, row=3, pady=5)

        tk.Label(self.Frames.CGR, justify="left", anchor="w", text="Find:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=4)
        self.data.Find = tk.Text(self.Frames.CGR, width=40, height=1)
        self.data.Find.grid(sticky='w', column=1, row=4, pady=5)

        tk.Label(self.Frames.CGR, justify="left", anchor="w", text="Token:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=5)
        self.data.Token = tk.Text(self.Frames.CGR, width=40, height=1)
        self.data.Token.grid(sticky='w', column=1, row=5, pady=5)

        tk.Button(self.Frames.CGR, text="Finish", command=self.SetUpdate, background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(stick='s', pady=20)

    def SetUpdate(self):
        Organization = self.data.Organization.get("1.0", "end-1c")
        Repository = self.data.Repository.get("1.0", "end-1c")
        Branch = self.data.Branch.get("1.0", "end-1c")
        VersionPath = self.data.VersionPath.get("1.0", "end-1c")
        Find = self.data.Find.get("1.0", "end-1c")
        Token = self.data.Token.get("1.0", "end-1c")

        self.Configuration['Update']['Organization'] = Organization
        self.Configuration['Update']['Repository'] = Repository
        self.Configuration['Update']['Branch'] = Branch
        self.Configuration['Update']['VersionPath'] = VersionPath
        self.Configuration['Update']['Find'] = Find
        if Token == "": 
            self.Configuration['Update']['Token'] = None
        else:
            self.Configuration['Update']['Token'] = Token
        self.data = self.Storage()
        self.ConfigStatus[1] = True
        self.UpdateStatus()
        print(str(self.Configuration.data['Update']))

    def ConfigureLaunch(self):
        self.ClearConfigure()
        self.Configuring = True
        self.data.errorcode = []
        self.data.arguments = []
        self.data.codelist = []

        self.fr_cfr_title.config(text="Launch Configuration")


        self.Frames.CGR_ProjectPath = tk.Frame(self.Frames.CGR, background=c.FRAME_BG1)
        self.Frames.CGR_ProjectPath.grid(sticky='w', column=0, row=0, pady=5)
        tk.Label(self.Frames.CGR_ProjectPath, justify="left", anchor="w", text="Project Path:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=0)
        self.data.ProjectPath = tk.Text(self.Frames.CGR_ProjectPath, width=30, height=1)
        self.data.ProjectPath.grid(sticky='w', column=1, row=0)

        self.Frames.CGR_ProjectMain = tk.Frame(self.Frames.CGR, background=c.FRAME_BG1)
        self.Frames.CGR_ProjectMain.grid(sticky='w', column=0, row=1, pady=5)
        tk.Label(self.Frames.CGR_ProjectMain, justify="left", anchor="w", text="Project Main:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=0)
        self.data.ProjectMain = tk.Text(self.Frames.CGR_ProjectMain, width=30, height=1)
        self.data.ProjectMain.grid(sticky='w', column=1, row=0)

        self.Frames.CGR_ErrorCodes = tk.Frame(self.Frames.CGR, background=c.FRAME_BG1)
        self.Frames.CGR_ErrorCodes.grid(sticky='w', column=0, row=2)
        tk.Label(self.Frames.CGR_ErrorCodes, justify="left", anchor="w", text="Error Codes:", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(sticky='w', column=0, row=0)
        tk.Label(self.Frames.CGR_ErrorCodes, width=10, text="Code", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(column=2, row=0)
        tk.Label(self.Frames.CGR_ErrorCodes, width=10, text="Arguments", background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(column=3, row=0) 
        tk.Button(self.Frames.CGR_ErrorCodes, text="Remove", command=self.RemoveCode, background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(column=4, row=0)

        self.data.ErrorCode = tk.Text(self.Frames.CGR_ErrorCodes, width=20, height=1)
        self.data.ErrorCode.grid(sticky='w', column=0, row=1, padx=5)
        tk.Button(self.Frames.CGR_ErrorCodes, text="Add", command=self.AddCode, background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(column=1, row=1, padx=5)

        tk.Button(self.Frames.CGR, text="Finish", command=self.SetLaunch, background=c.FRAME_BG1, foreground=c.LABEL_FG).grid(stick='s', pady=20)

    def DrawCodeList(self):
        for row in self.data.codelist:
            for item in row:
                item.destroy()
        self.data.codelist = []
        index = 0
        for code, arg in zip(self.data.errorcode, self.data.arguments):
            codeLabel = tk.Label(self.Frames.CGR_ErrorCodes, justify="left", anchor="w", text=code, background=c.FRAME_BG1, foreground=c.LABEL_FG)
            codeLabel.grid(sticky='w', column=2, row=index + 1)
            argLabel = tk.Label(self.Frames.CGR_ErrorCodes, justify="left", anchor="w", text=arg, background=c.FRAME_BG1, foreground=c.LABEL_FG)
            argLabel.grid(sticky='w', column=3, row=index + 1)
            self.data.codelist.append([codeLabel, argLabel])
            index += 1

    def AddCode(self):
        code = self.data.ErrorCode.get("1.0", "end-1c")
        if not ":" in code:
            return
        code = code.split(":")
        if len(code) > 2:
            return
        try:
            errorCode = int(code[0])
        except ValueError:
            return
        self.data.errorcode.append(code[0])
        self.data.arguments.append(code[1])
        self.DrawCodeList()

    def RemoveCode(self):
        if len(self.data.errorcode) == 0:
            return
        self.data.errorcode.pop()
        self.data.arguments.pop()
        self.DrawCodeList()

    def SetLaunch(self):
        self.Configuration['Launch']['ProjectRoot'] = self.data.ProjectPath.get("1.0", "end-1c")
        self.Configuration['Launch']['ProjectMain'] = self.data.ProjectMain.get("1.0", "end-1c")
        for code, arg in zip(self.data.errorcode, self.data.arguments):
            self.Configuration['Launch'][code] = arg
        self.data = self.Storage()
        self.ConfigStatus[2] = True
        self.UpdateStatus()
        print(str(self.Configuration.data['Launch']))
