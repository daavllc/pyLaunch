
import tkinter as tk
from tkinter import ttk
import webbrowser
import time

import helpers.config as config
from helpers.style import Style
import helpers.gui as gh
from helpers.logger import Logger
s = Style.Get()

class GUI:
    def __init__(self, configurator):
        self.Configurator = configurator
        self.log = Logger("pyLaunch.GUI", "gui.log")
    class Storage:
        pass
    def Launch(self):
        self.Initialize()
        self.Runtime()
        return self.Completed

    def Reset(self):
        self.ws = tk.Tk()

        self.Completed = False
        self.ConfigStatus = [False, False, False]
        self.Configuring = False
    
        self.data = self.Storage()
        self.Frames = self.Storage()
        self.Menus = self.Storage()

    def SetTheme(self, theme: str):
        s.Set(theme)
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
        self.Menus.Help.add_command(label="Documentation", command=lambda: webbrowser.open("https://docs.daav.us/pyLaunch"))
        self.Menus.Help.add_separator()
        self.Menus.Help.add_command(label="Configuration", command=self.PopupConfiguration)
        self.Menus.Help.add_command(label="Updater", command=self.PopupUpdater)
        self.Menus.Help.add_command(label="Setup", command=self.PopupSetup)
        self.Menus.Help.add_command(label="Launcher", command=self.PopupLauncher)

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

        gh.Button(self.Frames.Configuration_Body, text="Updater", command=self.ConfigureUpdater, width=8, bg=0).grid(column=0, row=1, padx=5, pady=5)
        self.fr_cft_update_status = gh.SmallLabel(self.Frames.Configuration_Body, text="Incomplete", bg=0)
        self.fr_cft_update_status.grid(column=1, row=1)

        gh.Button(self.Frames.Configuration_Body, text="Setup", command=self.ConfigureSetup, width=8, bg=0).grid(column=0, row=2, padx=5, pady=5)
        self.fr_cft_setup_status = gh.Label(self.Frames.Configuration_Body, text="Incomplete", font=s.FONT_TEXT_SMALL, bg=0)
        self.fr_cft_setup_status.grid(column=1, row=2)

        gh.Button(self.Frames.Configuration_Body, text="Launcher", command=self.ConfigureLauncher, width=8, bg=0).grid(column=0, row=3, padx=5, pady=5)
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
        popup = tk.Toplevel(self.ws, borderwidth=10, background=s.FRAME_BG_ALT)
        popup.geometry("350x270")
        popup.title("No valid configuration")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        gh.Title(popup, text="This project has no configuration", bg=1).pack()
        gh.Label(popup, text="If you're not the developer of this program,\nlet them know: 'pyLaunch has no configuration'\nTo use this program otherwise, launch it directly.", justify='left', bg=0).pack()

        gh.LargeLabel(popup, text="Developers:", justify='left', bg=1).pack(anchor='w', padx=5, pady=5)
        gh.Label(popup, text="Please set up each configuration on the left", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="then press finish to save it.", bg=1).pack(anchor='w', padx=s.PAD_BODY)
        gh.Label(popup, text="If you need any assistance, please check our docs page,\nthe 'help' menu or check our GitHub page").pack()

        Startup_Buttons = tk.Frame(popup, background=s.FRAME_BG_ALT)
        Startup_Buttons.pack(pady=5)
        gh.Button(Startup_Buttons, text="GitHub Page", command=lambda: webbrowser.open("https://github.com/daavofficial/pyLaunch"), bg=1).grid(column=0, row=0, padx=20)
        gh.Button(Startup_Buttons, text="Docs", command=lambda: webbrowser.open("https://docs.daav.us/pyLaunch"), width=6, bg=1).grid(sticky='w', column=1, row=0)
        gh.Button(Startup_Buttons, text="Close", command=popup.destroy, bg=1).grid(column=2, row=0, padx=20)
    
    def PopupAbout(self):
        popup = tk.Toplevel(self.ws, borderwidth=10, background=s.FRAME_BG_ALT)
        popup.geometry("350x300")
        popup.title("About")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        About_Title = tk.Frame(popup, background=s.FRAME_BG_ALT)
        About_Title.pack(anchor='w', pady=2)
        gh.Title(About_Title, text=f"pyLaunch {config.VERSION}", justify='left', bg=1).grid(sticky='s', column=0, row=0)
        gh.SmallLabel(About_Title, text=f"©2022 DAAV, LLC", justify='left', bg=1).grid(sticky='s', column=1, row=0)

        gh.Label(popup, text=f"Python project setup, updater, and launcher", bg=1).pack(anchor='w', padx=s.PAD_BODY)

        About_Source = tk.Frame(popup, borderwidth=10, background=s.FRAME_BG_ALT)
        About_Source.pack(anchor='w')
        gh.Label(About_Source, text=f"License: MIT", justify='left', bg=1).grid(sticky='w', column=0, row=0)
        gh.Button(About_Source, text="Source Code", command=lambda: webbrowser.open("https://github.com/daavofficial/pyLaunch"), bg=1).grid(sticky='w', column=1, row=0, padx=10)
        gh.Label(About_Source, text=f"Documentation: ", justify='left', bg=1).grid(sticky='w', column=0, row=1)
        gh.Button(About_Source, text="docs.daav.us", command=lambda: webbrowser.open("https://docs.daav.us/pyLaunch"), bg=1).grid(sticky='w', column=1, row=1, padx=10)

        gh.FillHorizontalSeparator(popup, pady=5)

        gh.Label(popup, text=f"GUI v{config.VERSION_CONFIGURATOR_GUI}", bg=1).pack(anchor='w', padx=5)
        gh.Label(popup, text=f"Configurator v{config.VERSION_CONFIGURATOR}", bg=1).pack(anchor='w', padx=5)
        gh.Label(popup, text=f"Configuration v{config.VERSION_CONFIGURATOR}", bg=1).pack(anchor='w', padx=5)
        gh.Label(popup, text=f"Updater v{config.VERSION_UPDATE}", bg=1).pack(anchor='w', padx=5)
        gh.Label(popup, text=f"Setup v{config.VERSION_SETUP}", bg=1).pack(anchor='w', padx=5)
        gh.Label(popup, text=f"Launcher v{config.VERSION_LAUNCH}", bg=1).pack(anchor='w', padx=5)

    def PopupConfiguration(self):
        popup = tk.Toplevel(self.ws, borderwidth=10, background=s.FRAME_BG_ALT)
        popup.geometry("350x200")
        popup.title("Help - Configuration")
        popup.resizable(width=False, height=False)
        popup.iconbitmap(self.Icon)

        gh.LargeLabel(popup, text="Configuration is broken into 3 parts:", bg=1).pack(pady=5)
        Config_Details = tk.Frame(popup, background=s.FRAME_BG_ALT)
        Config_Details.pack(pady=5)

        gh.Button(Config_Details, text="Updater", command=self.PopupUpdater, width=8, bg=1).grid(sticky='w', column=0, row=0)
        gh.Label(Config_Details, text="GitHub details for update checking/downloading", bg=1).grid(sticky='w', column=1, row=0, pady=5)

        gh.Button(Config_Details, text="Setup", command=self.PopupSetup, width=8, bg=1).grid(sticky='w', column=0, row=1)
        gh.Label(Config_Details, text="Dependancy installation", bg=1).grid(sticky='w', column=1, row=1, pady=5)

        gh.Button(Config_Details, text="Launcher", command=self.PopupLauncher, width=8, bg=1).grid(sticky='w', column=0, row=2)
        gh.Label(Config_Details, text="Error catching, and Python reloading", bg=1).grid(sticky='w', column=1, row=2, pady=5)

        Configuration_Buttons = tk.Frame(popup, background=s.FRAME_BG_ALT)
        Configuration_Buttons.pack(pady=5)

        gh.Label(Configuration_Buttons, text="More documentation is available at", bg=1).grid(sticky='w', column=0, row=0, pady=5)
        gh.Button(Configuration_Buttons, text="docs.daav.us", command=lambda: webbrowser.open("https://docs.daav.us/pyLaunch"), bg=1).grid(sticky='w', column=1, row=0)

    def PopupUpdater(self):
        popup = tk.Toplevel(self.ws, borderwidth=10, background=s.FRAME_BG_ALT)
        popup.geometry("400x355")
        popup.title("Help - Updater")
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

    def PopupSetup(self):
        popup = tk.Toplevel(self.ws, borderwidth=10, background=s.FRAME_BG_ALT)
        popup.geometry("420x320")
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

    def PopupLauncher(self):
        popup = tk.Toplevel(self.ws, borderwidth=10, background=s.FRAME_BG_ALT)
        popup.geometry("420x270")
        popup.title("Help - Launcher")
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
            self.Configurator.Save()
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
        self.data = self.Storage()
        self.fr_cfr_title.config(text="Select a configuration on the left")
        for item in self.Frames.CGR.winfo_children():
            item.destroy()
        if self.fr_cfr_popup_btn is not None:
            self.fr_cfr_popup_btn.destroy()
            self.fr_cfr_popup_btn = None

##########################################################################################
#
#                                UPDATER
#
##########################################################################################
    def ConfigureUpdater(self):
        self.ClearConfigure()
        self.Configuring = True
        self.fr_cfr_title.config(text="Updater Configuration")

        self.data.Update = {'SkipCheck' : tk.BooleanVar()}

        gh.Checkbutton(self.Frames.CGR, text="Skip update checking", variable=self.data.Update['SkipCheck'], command=self.SkipUpdate).grid(sticky='w', column=0, row=0)

        row = 1
        for text in ['Organization', 'Repository', 'Branch', 'Version Path', 'Find', 'Token']:
            gh.Label(self.Frames.CGR, justify="left", text=text + ":", bg=0).grid(sticky='w', column=0, row=row)
            self.data.Update[text.replace(" ", "")] = gh.Text(self.Frames.CGR, width=40, height=1)
            self.data.Update[text.replace(" ", "")].grid(sticky='w', column=1, row=row, pady=5)
            row += 1

        self.Frames.CGR_UpdateButtons = tk.Frame(self.Frames.CGR, background=s.FRAME_BG)
        self.Frames.CGR_UpdateButtons.grid(sticky='w', column=0, row=row, pady=5)
        self.StatusLabel = gh.LargeLabel(self.Frames.CGR_UpdateButtons, text="", bg=0)
        self.StatusLabel.grid(sticky='s')
        gh.Button(self.Frames.CGR_UpdateButtons, text="Finish", command=self.SetUpdate, bg=1).grid(sticky='s', pady=20)

    def SkipUpdate(self):
        self.Configurator.Update.SetSkipCheck(self.data.Update['SkipCheck'].get())

    def SetUpdate(self):
        self.StatusLabel.config(text="Verifiying information with GitHub...")

        Organization = self.data.Update['Organization'].get("1.0", "end-1c")
        Repository = self.data.Update['Repository'].get("1.0", "end-1c")
        Branch = self.data.Update['Branch'].get("1.0", "end-1c")
        VersionPath = self.data.Update['VersionPath'].get("1.0", "end-1c")
        Find = self.data.Update['Find'].get("1.0", "end-1c")
        Token = self.data.Update['Token'].get("1.0", "end-1c")

        if not type(self.data.Update['SkipCheck']) == bool:
            self.data.Update['SkipCheck'] = False

        status = self.Configurator.Update.Set(Organization, Repository, Branch, VersionPath, Find, Token, self.data.Update['SkipCheck'])
        if not type(status) == list:
            self.StatusLabel.config(text="Unable to connect to the internet, config saved.")
            self.ConfigStatus[1] = True
            self.UpdateStatus()
        elif all(element == None for element in status):
            self.ConfigStatus[1] = True
            self.UpdateStatus()
            self.StatusLabel.config(text="Done!")
            self.ClearConfigure()
            self.log.info(f"Stored Update: {self.Configurator.Configuration.data['Update']}")
        else:
            for stat in status:
                if stat is not None:
                    self.StatusLabel.config(text=stat)
                    break
            self.log.info(f"Update configuration issues: {str(status)}")

##########################################################################################
#
#                                SETUP
#
##########################################################################################
    def ConfigureSetup(self):
        self.ClearConfigure()
        self.Configuring = True
        self.data.packages = {}
        self.data.tk_items = []

        self.fr_cfr_title.config(text="Setup Configuration", background=s.FRAME_BG_ALT, foreground=s.LABEL_FG)

        self.Frames.CGR_PythonVersion = tk.Frame(self.Frames.CGR, background=s.FRAME_BG)
        self.Frames.CGR_PythonVersion.grid(sticky='w', column=0, row=0, pady=5)
        gh.Label(self.Frames.CGR_PythonVersion, justify="left", text="Python Version:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.PythonVersion = gh.Text(self.Frames.CGR_PythonVersion, width=5, height=1, bg=0)
        self.data.PythonVersion.grid(sticky='w', column=1, row=0, padx=5, pady=5)

        self.Frames.CGR_MinimumPythonVersion = tk.Frame(self.Frames.CGR, background=s.FRAME_BG)
        self.Frames.CGR_MinimumPythonVersion.grid(sticky='w', column=0, row=1, pady=5)
        gh.Label(self.Frames.CGR_MinimumPythonVersion, justify="left", text="Minimum Python Version:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.MinimumPythonVersion = gh.Text(self.Frames.CGR_MinimumPythonVersion, width=5, height=1, bg=0)
        self.data.MinimumPythonVersion.grid(sticky='w', column=1, row=0, padx=5, pady=5)
        
        self.Frames.CGR_Packages = tk.Frame(self.Frames.CGR, background=s.FRAME_BG)
        self.Frames.CGR_Packages.grid(sticky='w', column=0, row=2, pady=5)

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

        self.StatusLabel = gh.Label(self.Frames.CGR_Package_Input, text="", width=20, wraplength=200, bg=0)
        self.StatusLabel.grid(sticky='s')
        gh.Button(self.Frames.CGR_Package_Input, text="Finish", command=self.SetSetup, bg=1).grid(sticky='s', pady=20)

    def DrawPackageList(self):
        for row in self.data.tk_items:
            for item in row:
                item.destroy()
        self.data.tk_items = []
        index = 0
        for py, imp in self.data.packages.items():
            bg = 0
            if index % 2:
                bg = 1
            pyNameLabel = gh.Label(self.Frames.CGR_Table, text=py, justify="left", bg=bg)
            pyNameLabel.grid(sticky='w', column=0, row=index + 1)
            importNameLabel = gh.Label(self.Frames.CGR_Table, text=imp, justify="left", bg=bg)
            importNameLabel.grid(sticky='w', column=1, row=index + 1)
            removeButton = gh.Button(self.Frames.CGR_Table, text="Remove", command=lambda key=py, index=index: self.RemovePackage(index, key), bg=0)
            removeButton.grid(column=2, row=index + 1, padx=5, pady=1)
            self.data.tk_items.append([pyNameLabel, importNameLabel, removeButton])
            index += 1

    def AddPackage(self):
        package = self.data.PackageName.get("1.0", "end-1c")
        if ":" in package:
            if self.data.packages.get(package[0], None) is None:
                package = package.split(":")
                self.data.packages[package[0]] = package[1]
        else:
            if self.data.packages.get(package, None) is None:
                self.data.packages[package] = package
        self.DrawPackageList()

    def RemovePackage(self, index:int, key: str):
        del self.data.packages[key]
        for item in self.data.tk_items.pop(index):
            item.destroy()
        self.DrawPackageList()

    def SetSetup(self):
        status = self.Configurator.Setup.Set(self.data.PythonVersion.get("1.0", "end-1c"), 
                        self.data.MinimumPythonVersion.get("1.0", "end-1c"), self.data.packages)

        if all(element == None for element in status):
            self.ConfigStatus[0] = True
            self.UpdateStatus()
            self.StatusLabel.config(text="Done!")
            self.ClearConfigure()
            self.log.info(f"Stored Setup: {self.Configurator.Configuration.data['Setup']}")
        else:
            for stat in status:
                if stat is not None:
                    self.StatusLabel.config(text=stat)
                    break
            self.log.info(f"Setup configuration issues: {str(status)}")


##########################################################################################
#
#                                LAUNCH
#
##########################################################################################
    def ConfigureLauncher(self):
        self.ClearConfigure()
        self.Configuring = True

        self.fr_cfr_title.config(text="Launcher Configuration")

        self.data.codes = {}
        self.data.tk_items = []
        self.data.LaunchSkipCheck = tk.BooleanVar()

        gh.Checkbutton(self.Frames.CGR, text="Skip update checking", variable=self.data.LaunchSkipCheck, command=self.SkipLaunchErrors).grid(sticky='w', column=0, row=0)

        self.Frames.CGR_ProjectPath = tk.Frame(self.Frames.CGR, background=s.FRAME_BG_ALT)
        self.Frames.CGR_ProjectPath.grid(sticky='w', column=0, row=1, pady=5)
        gh.Label(self.Frames.CGR_ProjectPath, justify="left", text="Project Root:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.ProjectPath = gh.Text(self.Frames.CGR_ProjectPath, width=30, height=1)
        self.data.ProjectPath.grid(sticky='w', column=1, row=0)

        self.Frames.CGR_ProjectMain = tk.Frame(self.Frames.CGR, background=s.FRAME_BG_ALT)
        self.Frames.CGR_ProjectMain.grid(sticky='w', column=0, row=2, pady=5)
        gh.Label(self.Frames.CGR_ProjectMain, justify="left", text="Project Main:", bg=0).grid(sticky='w', column=0, row=0)
        self.data.ProjectMain = gh.Text(self.Frames.CGR_ProjectMain, width=30, height=1)
        self.data.ProjectMain.grid(sticky='w', column=1, row=0)

        self.Frames.CGR_ErrorCodes = tk.Frame(self.Frames.CGR, background=s.FRAME_BG)
        self.Frames.CGR_ErrorCodes.grid(sticky='w', column=0, row=3)

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

        self.StatusLabel = gh.Label(self.Frames.CGR_ErrorCodes_Input, text="", width=20, wraplength=200, bg=0)
        self.StatusLabel.grid(sticky='s')
        gh.Button(self.Frames.CGR_ErrorCodes_Input, text="Finish", command=self.SetLaunch, bg=1).grid(sticky='s', pady=20)

    def SkipLaunchErrors(self):
        self.Configurator.Launch.SetSkipCheck(self.data.LaunchSkipCheck.get())

    def DrawCodeList(self):
        for row in self.data.tk_items:
            for item in row:
                item.destroy()
        self.data.tk_items = []
        index = 0
        for code, arg in self.data.codes.items():
            bg = 0
            if index % 2:
                bg = 1
            pyNameLabel = gh.Label(self.Frames.CGR_ErrorCodes_Table, text=code, justify="left", bg=bg)
            pyNameLabel.grid(sticky='w', column=0, row=index + 1)
            importNameLabel = gh.Label(self.Frames.CGR_ErrorCodes_Table, text=arg, justify="left", bg=bg)
            importNameLabel.grid(sticky='w', column=1, row=index + 1)
            removeButton = gh.Button(self.Frames.CGR_ErrorCodes_Table, text="Remove", command=lambda key=code, index=index: self.RemoveCode(index, key), bg=0)
            removeButton.grid(column=2, row=index + 1, padx=5, pady=1)
            self.data.tk_items.append([pyNameLabel, importNameLabel, removeButton])
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
        self.data.codes[code[0]] = code[1]
        self.DrawCodeList()

    def RemoveCode(self, index: int, key: str):
        del self.data.codes[key]
        for item in self.data.tk_items.pop(index):
            item.destroy()
        self.DrawCodeList()

    def SetLaunch(self):
        ProjectRoot = self.data.ProjectPath.get("1.0", "end-1c")
        ProjectMain = self.data.ProjectMain.get("1.0", "end-1c")
        SkipCheck = self.data.LaunchSkipCheck.get()

        status = self.Configurator.Launch.Set(ProjectRoot, ProjectMain, self.data.codes, SkipCheck)
        if all(element == None for element in status):
            self.data = self.Storage()
            self.ConfigStatus[2] = True
            self.UpdateStatus()
            self.StatusLabel.config(text="Done!")
            self.ClearConfigure()
            self.log.info(f"Stored Update: {self.Configurator.Configuration.data['Launch']}")
        else:
            for stat in status:
                if stat is not None:
                    self.StatusLabel.config(text=stat)
                    break
            self.log.info(f"Launch configuration issues: {str(status)}")
