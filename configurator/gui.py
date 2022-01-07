
import tkinter as tk
from tkinter import ttk
import webbrowser

from .configuration import Configuration
from .serializer import Serialize
import helpers.config as config
from helpers.style import Style
import helpers.gui as gh
s = Style.Get()

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

    def SetTheme(self, theme: str):
        s.Set(theme)
        self.ws.destroy()
        self.Initialize()

    def DarkMode(self):
        s.Set('dark')
        self.ws.destroy()
        self.Initialize()

    def LightMode(self):
        s.Set('light')
        self.ws.destroy()
        self.Initialize()

    def Initialize(self):
        self.Reset()
        self.ws.title(f"pyLaunch Configurator {config.VERSION}")
        self.ws.geometry("700x400")
        self.ws.resizable(width=False, height=False)
        self.Icon = tk.PhotoImage(f"{config.PATH_ROOT}/pyLaunch.ico")
        self.ws.iconbitmap(self.Icon)

        # Menu
        self.Menus.Main = tk.Menu(self.ws)
        self.ws.config(menu=self.Menus.Main)

        # View
        self.Menus.View = tk.Menu(self.Menus.Main, tearoff=0, background=s.FRAME_BG_ALT, foreground=s.LABEL_FG)
        self.Menus.Main.add_cascade(label="View", menu=self.Menus.View)
        self.Menus.View_Themes = tk.Menu(self.Menus.View, tearoff=0, background=s.FRAME_BG_ALT, foreground=s.LABEL_FG)
        self.Menus.View.add_cascade(label="Themes", menu=self.Menus.View_Themes)

        for theme in s.GetThemes():
            self.Menus.View_Themes.add_command(label=theme, command=lambda theme=theme: self.SetTheme(theme))
        #self.Menus.View.add_command(label="Dark mode", command=self.DarkMode)
        #self.Menus.View.add_command(label="Light mode", command=self.LightMode)

        # Help
        self.Menus.Help = tk.Menu(self.Menus.Main, tearoff=0, background=s.FRAME_BG_ALT, foreground=s.LABEL_FG)
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
        self.Frames.Configuration = tk.Frame(self.ws, width=200, height=400, borderwidth=10, background=s.FRAME_BG)
        self.Frames.Configuration.grid_propagate(0)
        self.Frames.Configuration.pack(fill='both', side='left', expand='True')

        self.Frames.Configuration_Title = tk.Frame(self.Frames.Configuration, background=s.FRAME_BG)
        self.Frames.Configuration_Title.pack_propagate(0)
        self.Frames.Configuration_Title.pack(fill='both', side='top', expand='False')
        gh.Title(self.Frames.Configuration_Title, text="Configurations", bg=0).grid(column=0, row=0)

        self.Frames.Configuration_Body = tk.Frame(self.Frames.Configuration, background=s.FRAME_BG)
        self.Frames.Configuration_Body.pack_propagate(0)
        self.Frames.Configuration_Body.pack(fill='both', side='top', expand='False')
        gh.Button(self.Frames.Configuration_Body, text="Setup", command=self.ConfigureSetup, width=8, bg=0).grid(column=0, row=1, padx=5, pady=5)

        self.fr_cft_setup_status = gh.Label(self.Frames.Configuration_Body, text="Incomplete", font=s.FONT_TEXT_SMALL, bg=0)
        self.fr_cft_setup_status.grid(column=1, row=1)
        gh.Button(self.Frames.Configuration_Body, text="Update", command=self.ConfigureUpdate, width=8, bg=0).grid(column=0, row=2, padx=5, pady=5)
        self.fr_cft_update_status = gh.SmallLabel(self.Frames.Configuration_Body, text="Incomplete", bg=0)
        self.fr_cft_update_status.grid(column=1, row=2)
        gh.Button(self.Frames.Configuration_Body, text="Launch", command=self.ConfigureLaunch, width=8, bg=0).grid(column=0, row=3, padx=5, pady=5)
        self.fr_cft_launch_status = gh.SmallLabel(self.Frames.Configuration_Body, text="Incomplete", bg=0)
        self.fr_cft_launch_status.grid(column=1, row=3)

        self.fr_cft_finish_label = gh.Label(self.Frames.Configuration_Body, text="", bg=0)
        self.fr_cft_finish_label.grid(column=0, row=4)
        gh.Button(self.Frames.Configuration_Body, text="Finish", command=self.FinishConfiguration, bg=0).grid(column=0, row=5)

        # Configurator
        self.Frames.Configurator = tk.Frame(self.ws, width=500, height=400, borderwidth=10, background=s.FRAME_BG_ALT)
        self.Frames.Configurator.grid_propagate(0)
        self.Frames.Configurator.pack(fill='both', side='right', expand='True')
        self.fr_cfr_title = gh.Title(self.Frames.Configurator, text="Select a configuration on the left", bg=1)
        self.fr_cfr_title.grid(column=0, row=0)
        self.fr_cfr_popup_btn = gh.Button(self.Frames.Configurator, text="What's this?", command=self.PopupStartup, bg=1)
        self.fr_cfr_popup_btn.grid(sticky="e", column=1, row=0, padx=50)
        self.Frames.CGR = tk.Frame(self.Frames.Configurator, width=500, height=325, borderwidth=10, background=s.FRAME_BG)
        self.Frames.CGR.grid_propagate(0)
        self.Frames.CGR.pack(fill='both', side='bottom', expand='False')

    def PopupStartup(self):
        popup = tk.Toplevel(self.ws, background=s.FRAME_BG_ALT)
        popup.geometry("350x250")
        popup.title("No valid configuration")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        gh.Title(popup, text="This project has no configuration", bg=1).pack()
        gh.Label(popup, text="If you're not the developer of this program,\nlet them know: 'pyLaunch has no configuration'\nTo use this program otherwise, launch it directly.", justify='left', bg=0).pack()

        gh.LargeLabel(popup, text="Developers:", justify='left', bg=1).pack(anchor='w', padx=5, pady=5)
        gh.Label(popup, text="Please set up each configuration on the left", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="then press finish to save it.", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="If you need any assistance, check the 'help' menu for\ninformation or check our GitHub page").pack()

        Startup_Buttons = tk.Frame(popup, background=s.FRAME_BG_ALT)
        Startup_Buttons.pack(pady=5)
        gh.Button(Startup_Buttons, text="GitHub Page", command=lambda: webbrowser.open("https://github.com/daavofficial/pyLaunch"), justify='left', bg=1).grid(column=0, row=0, padx=30)
        gh.Button(Startup_Buttons, text="Close", command=popup.destroy, bg=1).grid(column=1, row=0)
    
    def PopupAbout(self):
        popup = tk.Toplevel(self.ws, background=s.FRAME_BG_ALT)
        popup.geometry("350x200")
        popup.title("About")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        About_Title = tk.Frame(popup, background=s.FRAME_BG_ALT)
        About_Title.pack(anchor='w', pady=2)
        gh.Title(About_Title, text=f"pyLaunch {config.VERSION}", justify='left', bg=1).grid(sticky='s', column=0, row=0)
        gh.SmallLabel(About_Title, text=f"©2022 DAAV, LLC", justify='left', bg=1).grid(sticky='s', column=1, row=0)

        gh.Label(popup, text=f"Python project setup, updater, and pyLaunch", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        About_Source = tk.Frame(popup, background=s.FRAME_BG_ALT)
        About_Source.pack(anchor='w')
        gh.Label(About_Source, text=f"License: MIT", justify='left', bg=1).grid(sticky='w', column=0, row=0)
        gh.Button(About_Source, text="Source Code", command=lambda: webbrowser.open("https://github.com/daavofficial/pyLaunch"), bg=1).grid(sticky='w', column=1, row=0, padx=10)

        gh.FillHorizontalSeparator(popup, pady=5)

        gh.Label(popup, text=f"GUI v{config.VERSION_GUI}", bg=1).pack(anchor='w', padx=5)
        gh.Label(popup, text=f"Project Launch v{config.VERSION_PROJECT_LAUNCH}", bg=1).pack(anchor='w', padx=5)
        gh.Label(popup, text=f"Project Setup v{config.VERSION_PROJECT_SETUP}", bg=1).pack(anchor='w', padx=5)
        gh.Label(popup, text=f"Project Update v{config.VERSION_PROJECT_UPDATE}", bg=1).pack(anchor='w', padx=5)

    def PopupConfiguration(self):
        popup = tk.Toplevel(self.ws, background=s.FRAME_BG_ALT)
        popup.geometry("350x150")
        popup.title("Help - Configuration")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        gh.LargeLabel(popup, text="Configuration is broken into 3 parts:", bg=1).pack(pady=5)
        Config_Details = tk.Frame(popup, background=s.FRAME_BG_ALT)
        Config_Details.pack(pady=5)
        gh.Button(Config_Details, text="Setup", command=self.PopupSetup, width=6, bg=1).grid(sticky='w', column=0, row=0)
        gh.Label(Config_Details, text="Required python version, required packages", bg=1).grid(sticky='w', column=1, row=0, pady=5)

        gh.Button(Config_Details, text="Update", command=self.PopupUpdate, width=6, bg=1).grid(sticky='w', column=0, row=1)
        gh.Label(Config_Details, text="GitHub details for update checking/downloading", bg=1).grid(sticky='w', column=1, row=1, pady=5)

        gh.Button(Config_Details, text="Launch", command=self.PopupLaunch, width=6, bg=1).grid(sticky='w', column=0, row=2)
        gh.Label(Config_Details, text="Error catching, and python reloading", bg=1).grid(sticky='w', column=1, row=2, pady=5)

    def PopupSetup(self):
        popup = tk.Toplevel(self.ws, background=s.FRAME_BG_ALT)
        popup.geometry("400x300")
        popup.title("Help - Setup")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        gh.Label(popup, text="Setup simplifies installation by running python", bg=1).pack()
        gh.Label(popup, text="using your project's required version,", bg=1).pack()
        gh.Label(popup, text="and installing required packages automatically", bg=1).pack()

        gh.FillHorizontalSeparator(popup, pady=5)

        gh.LargeLabel(popup, text="Setup requires two things:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="The version of python your project uses", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="The packages your project depends on", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Python Version", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Provide the required python version (ex: 3.10)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Required packages:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Provide the pip install name, and the import name", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="If they are the same, just type the package name (ex: numpy)", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="If they are different, delimit them with a colon (ex: pyyaml:yaml)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

    def PopupUpdate(self):
        popup = tk.Toplevel(self.ws, background=s.FRAME_BG_ALT)
        popup.geometry("400x335")
        popup.title("Help - Update")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        gh.Label(popup, text="Check installed version vs most recent version on GitHub", bg=1).pack()

        gh.FillHorizontalSeparator(popup, pady=5)

        gh.LargeLabel(popup, text="Organization:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Your GitHub username (ex: daavofficial)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Repository:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Your GitHub repository's name (ex: pyLaunch)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Branch:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Branch to check (ex: main)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Version Path:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Repository path to the file that contains the version", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="(ex: /src/config.py)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Find:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="The string to look for to find the version (ex: VERSION = )", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Token:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Only needed for accessing private repositores", bg=1).pack(anchor='w', padx=s.PAD_BODY)

    def PopupLaunch(self):
        popup = tk.Toplevel(self.ws, background=s.FRAME_BG_ALT)
        popup.geometry("400x250")
        popup.title("Help - Launch")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        gh.Label(popup, text="Launch project and check error codes", bg=1).pack()

        gh.FillHorizontalSeparator(popup, pady=5)

        gh.LargeLabel(popup, text="Project Root:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Relative path from pyLaunch to your Project's root folder (ex: ..)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Project Main:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Repository path to your project's main file (ex: /start.py)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        gh.LargeLabel(popup, text="Error Codes:", bg=1).pack(anchor='w', padx=s.PAD_HEADERX)
        gh.Label(popup, text="Provide the error code and addional arguments", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="Error codes are formated as follows: 'code:args' (ex: -2:-UI GUI)", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="If you provide and error code with no arguments,", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="it will reload python (ex: -1:)", bg=1).pack(anchor='w', padx=s.PAD_BODY)

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

        self.fr_cfr_title.config(text="Setup Configuration", background=s.FRAME_BG_ALT, foreground=s.LABEL_FG)

        self.Frames.CGR_PythonVersion = tk.Frame(self.Frames.CGR, background=s.FRAME_BG)
        self.Frames.CGR_PythonVersion.grid(sticky='w', column=0, row=0, pady=5)
        gh.Label(self.Frames.CGR_PythonVersion, justify="left", text="Required Python Version:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.PythonVersion = gh.Text(self.Frames.CGR_PythonVersion, width=5, height=1, bg=0)
        self.data.PythonVersion.grid(sticky='w', column=1, row=0, padx=5, pady=5)
        
        self.Frames.CGR_Packages = tk.Frame(self.Frames.CGR, background=s.FRAME_BG)
        self.Frames.CGR_Packages.grid(sticky='w', column=0, row=1, pady=5)

        self.Frames.CGR_Package_Input = tk.Frame(self.Frames.CGR_Packages, background=s.FRAME_BG)
        self.Frames.CGR_Package_Input.grid(sticky='n', column=0, row=0, padx=5)
        gh.Label(self.Frames.CGR_Package_Input, justify="left", text="Packages:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.PackageName = gh.Text(self.Frames.CGR_Package_Input, width=20, height=1, bg=0)
        self.data.PackageName.grid(sticky='w', column=0, row=1, padx=5, pady=5)
        gh.Button(self.Frames.CGR_Package_Input, text="Add", command=self.AddPackage, bg=0).grid(column=1, row=1, pady=5)

        self.Frames.CGR_Table = tk.Frame(self.Frames.CGR_Packages, background=s.FRAME_BG)
        self.Frames.CGR_Table.grid(sticky='n', column=1, row=0)
        gh.Label(self.Frames.CGR_Table, justify="left", width=10, text="pypiName", bg=1).grid(column=0, row=0)
        gh.Label(self.Frames.CGR_Table, justify="left", width=10, text="importName", bg=1).grid(column=1, row=0)

        gh.Button(self.Frames.CGR_Package_Input, text="Finish", command=self.SetSetup, bg=1).grid(stick='s', pady=20)

    def DrawPackageList(self):
        for row in self.data.packagelist:
            for item in row:
                item.destroy()
        self.data.packagelist = []
        index = 0
        for py, imp in zip(self.data.pypiName, self.data.importName):
            bg = 0
            if index % 2:
                bg = 1
            pyNameLabel = gh.Label(self.Frames.CGR_Table, text=py, justify="left", bg=bg)
            pyNameLabel.grid(sticky='w', column=0, row=index + 1)
            importNameLabel = gh.Label(self.Frames.CGR_Table, text=imp, justify="left", bg=bg)
            importNameLabel.grid(sticky='w', column=1, row=index + 1)
            removeButton = gh.Button(self.Frames.CGR_Table, text="Remove", command=lambda index=index: self.RemovePackage(index), bg=0)
            removeButton.grid(column=2, row=index + 1, padx=5, pady=1)
            self.data.packagelist.append([pyNameLabel, importNameLabel, removeButton])
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

    def RemovePackage(self, index: int):
        self.data.pypiName.pop(index)
        self.data.importName.pop(index)
        self.DrawPackageList()

    def SetSetup(self):
        self.Configuration['Setup']['PythonVersion'] = self.data.PythonVersion.get("1.0", "end-1c")
        self.Configuration['Setup']['PythonFolder'] = "Python" + self.Configuration['Setup']['PythonVersion'].replace(".", "")
        for py, imp in zip(self.data.pypiName, self.data.importName):
            self.Configuration['Setup']['Packages'][py] = imp
        self.data = self.Storage()
        self.ConfigStatus[0] = True
        self.UpdateStatus()
        self.ClearConfigure()
        print(str(self.Configuration.data['Setup']))

    def ConfigureUpdate(self):
        self.ClearConfigure()
        self.Configuring = True
        self.fr_cfr_title.config(text="Update Configuration")

        self.data.Update = {}
        row = 0
        for text in ['Organization', 'Repository', 'Branch', 'Version Path', 'Find', 'Token']:
            gh.Label(self.Frames.CGR, justify="left", text=text + ":", bg=0).grid(sticky='w', column=0, row=row)
            self.data.Update[text.replace(" ", "")] = gh.Text(self.Frames.CGR, width=40, height=1)
            self.data.Update[text.replace(" ", "")].grid(sticky='w', column=1, row=row, pady=5)
            row += 1

        gh.Button(self.Frames.CGR, text="Finish", command=self.SetUpdate, bg=1).grid(stick='s', pady=20)

    def SetUpdate(self):
        Organization = self.data.Update['Organization'].get("1.0", "end-1c")
        Repository = self.data.Update['Repository'].get("1.0", "end-1c")
        Branch = self.data.Update['Branch'].get("1.0", "end-1c")
        VersionPath = self.data.Update['VersionPath'].get("1.0", "end-1c")
        Find = self.data.Update['Find'].get("1.0", "end-1c")
        Token = self.data.Update['Token'].get("1.0", "end-1c")

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
        self.ClearConfigure()
        print(str(self.Configuration.data['Update']))

    def ConfigureLaunch(self):
        self.ClearConfigure()
        self.Configuring = True
        self.data.errorcode = []
        self.data.arguments = []
        self.data.codelist = []

        self.fr_cfr_title.config(text="Launch Configuration")

        self.Frames.CGR_ProjectPath = tk.Frame(self.Frames.CGR, background=s.FRAME_BG_ALT)
        self.Frames.CGR_ProjectPath.grid(sticky='w', column=0, row=0, pady=5)
        gh.Label(self.Frames.CGR_ProjectPath, justify="left", text="Project Path:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.ProjectPath = gh.Text(self.Frames.CGR_ProjectPath, width=30, height=1)
        self.data.ProjectPath.grid(sticky='w', column=1, row=0)

        self.Frames.CGR_ProjectMain = tk.Frame(self.Frames.CGR, background=s.FRAME_BG_ALT)
        self.Frames.CGR_ProjectMain.grid(sticky='w', column=0, row=1, pady=5)
        gh.Label(self.Frames.CGR_ProjectMain, justify="left", text="Project Main:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.ProjectMain = gh.Text(self.Frames.CGR_ProjectMain, width=30, height=1)
        self.data.ProjectMain.grid(sticky='w', column=1, row=0)

        self.Frames.CGR_ErrorCodes = tk.Frame(self.Frames.CGR, background=s.FRAME_BG)
        self.Frames.CGR_ErrorCodes.grid(sticky='w', column=0, row=2)

        self.Frames.CGR_ErrorCodes_Input = tk.Frame(self.Frames.CGR_ErrorCodes, background=s.FRAME_BG)
        self.Frames.CGR_ErrorCodes_Input.grid(sticky='n', column=0, row=0)

        gh.Label(self.Frames.CGR_ErrorCodes_Input, justify="left", text="Error Codes:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.ErrorCode = gh.Text(self.Frames.CGR_ErrorCodes_Input, width=20, height=1, bg=0)
        self.data.ErrorCode.grid(sticky='w', column=0, row=1, padx=5)
        gh.Button(self.Frames.CGR_ErrorCodes_Input, text="Add", command=self.AddCode, bg=1).grid(column=1, row=1, padx=5, pady=5)

        self.Frames.CGR_ErrorCodes_Table = tk.Frame(self.Frames.CGR_ErrorCodes, background=s.FRAME_BG)
        self.Frames.CGR_ErrorCodes_Table.grid(sticky='n', column=1, row=0)
        
        gh.Label(self.Frames.CGR_ErrorCodes_Table, justify="left", width=10, text="Code", bg=1).grid(column=0, row=0)
        gh.Label(self.Frames.CGR_ErrorCodes_Table, justify="left", width=10, text="Arguments", bg=1).grid(column=1, row=0) 

        gh.Button(self.Frames.CGR_ErrorCodes_Input, text="Finish", command=self.SetLaunch, bg=1).grid(stick='s', pady=20)

    def DrawCodeList(self):
        for row in self.data.codelist:
            for item in row:
                item.destroy()
        self.data.codelist = []
        index = 0
        for code, arg in zip(self.data.errorcode, self.data.arguments):
            bg = 0
            if index % 2:
                bg = 1
            codeLabel = gh.Label(self.Frames.CGR_ErrorCodes_Table, justify="left", text=code, bg=bg)
            codeLabel.grid(sticky='w', column=0, row=index + 1)
            argLabel = gh.Label(self.Frames.CGR_ErrorCodes_Table, justify="left", text=arg, bg=bg)
            argLabel.grid(sticky='w', column=1, row=index + 1)
            removeButton = gh.Button(self.Frames.CGR_ErrorCodes_Table, text="Remove", command=lambda index=index: self.RemoveCode(index), bg=1)
            removeButton.grid(column=2, row=index + 1, padx=5, pady=1)
            self.data.codelist.append([codeLabel, argLabel, removeButton])
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

    def RemoveCode(self, index: int):
        self.data.errorcode.pop(index)
        self.data.arguments.pop(index)
        self.DrawCodeList()

    def SetLaunch(self):
        self.Configuration['Launch']['ProjectRoot'] = self.data.ProjectPath.get("1.0", "end-1c")
        self.Configuration['Launch']['ProjectMain'] = self.data.ProjectMain.get("1.0", "end-1c")
        for code, arg in zip(self.data.errorcode, self.data.arguments):
            self.Configuration['Launch'][code] = arg
        self.data = self.Storage()
        self.ConfigStatus[2] = True
        self.UpdateStatus()
        self.ClearConfigure()
        print(str(self.Configuration.data['Launch']))
