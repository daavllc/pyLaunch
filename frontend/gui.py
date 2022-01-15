import asyncio
import tkinter as tk
from tkinter import ttk
import time
import threading
import webbrowser

import helpers.config as config
from helpers.style import Style
import helpers.gui as gh

from frontend.update import Updater
from frontend.launch import Launcher
from frontend.setup import Setup

s = Style.Get()

class GUI:
    class _Storage:
        pass

    def Start(self):
        self.Initialize()
        self.Automatic()
    
    def Initialize(self):
        self.ws = tk.Tk()
        self.ws.title(f"pyLaunch")
        self.ws.geometry("400x300")
        self.ws.resizable(width=False, height=False)
        self.Icon = tk.PhotoImage(f"{config.PATH_ROOT}/pyLaunch.ico")
        self.ws.iconbitmap(self.Icon)

        self.Frames = self._Storage()
        self.Status = [False, False, False]

    def Runtime(self):
        self.ws.mainloop()

    def CreateThread(self):
        self.Thread = True
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._LaunchAutomatic())

    def Automatic(self):
        self.Init()
        thread = threading.Thread(target=self.CreateThread)
        thread.start()

        self.Runtime()
        if self.Status[0] and self.Status[1] and self.Status[2]:
            print("Launching!")
            self.Launch.Launch()
        else:
            print("Unable to launch [", end="")
            print("Update: ", end="")
            if self.Status[0]:
                print("Success", end="")
            else:
                print("Failure", end="")
            print(", Launch: ", end="")
            if self.Status[1]:
                print("Success", end="")
            else:
                print("Failure", end="")
            print(", Setup: ", end="")
            if self.Status[2]:
                print("Success", end="")
            else:
                print("Failure", end="")
            print("]")
        return

    async def _LaunchAutomatic(self):
        StartTime = time.perf_counter()
        while time.perf_counter() - StartTime < 0.1:
            pass

        if self.InitUpdate():
            if self.InitLaunch():
                self.InitSetup()
                self.ws.destroy()

    def Init(self):
        self.Frames.Header = tk.Frame(self.ws, width=400, height=60, borderwidth=10, background=s.FRAME_BG)
        self.Frames.Header.pack_propagate(0)
        self.Frames.Header.pack(fill='both', side='top', expand='False')

        self.StatusLabel = gh.LargeLabel(self.Frames.Header, text="", wraplength=250, bg=0)
        self.StatusLabel.pack()
        gh.FillHorizontalSeparator(self.Frames.Header, pady=5)

        self.Frames.Body = tk.Frame(self.ws, background=s.FRAME_BG_ALT)
        self.Frames.Body.pack(fill='both', side='left', expand='True')

    ### Update
    def InitUpdate(self) -> bool:
        self.ws.title(f"pyLaunch - Update")
        self.Update = Updater()
        self.Frames.Update = tk.Frame(self.Frames.Body, background=s.FRAME_BG)
        self.Frames.Update.pack(fill='both', side='top', expand='True')

        status = self.Update.CheckConnection()
        if type(status) == str:
            self.StatusLabel.config(text=status)
            self.Frames.Update.destroy()
            self.Status[0] = True
            return

        self.StatusLabel.config(text="Checking for update...")
        status = self.Update.CheckVersions()
        if type(status) == list:
            if status[1]: # Can still continue
                self.StatusLabel.config(text=status[0])
                self.FinishUpdate()
                return True
            else:
                self.StatusLabel.config(text=f"Error {status[0]}")
                print(f"Error: {status}")
                return False
        elif status:
            self.StatusLabel.config(text="An update is available")
            return self.UpdateLoop()
        else:
            self.StatusLabel.config(text="You have the latest version")
            self.FinishUpdate()
            return True

    def UpdateLoop(self) -> bool:
        self.UpdateSelected = False
        self.Frames.Update_Available = tk.Frame(self.Frames.Update, background=s.FRAME_BG)
        self.Frames.Update_Available.pack(fill='both', side='top', expand='True')
        gh.Label(self.Frames.Update_Available, text="Available").grid()

        gh.LargeLabel(self.Frames.Update_Available, text=f"Update from [v{'.'.join([str(sec) for sec in self.Update.Versions[0]])}] to [v{'.'.join([str(sec) for sec in self.Update.Versions[1]])}]?", bg=0).grid(column=0, row=0, pady=5)
        gh.Button(self.Frames.Update_Available, text="Yes", command=self.InstallUpdate, bg=0).grid(column=0, row=1)
        gh.Button(self.Frames.Update_Available, text="No", command=self.SkipUpdate, bg=0).grid(column=1, row=1)

        while self.UpdateSelected == False:
            pass
        return True

    def InstallUpdate(self):
        self.Frames.Update_Available.destroy()

        self.StatusLabel.config(text="Downloading update...")
        if not self.Update.DownloadUpdate():
            self.StatusLabel.config(text="Failed to download update")
        else:
            self.StatusLabel.config(text="Download complete! Installing...")

        if not self.Update.InstallUpdate():
            self.StatusLabel.config(text="Failed to install update")
        else:
            self.StatusLabel.config(text="Update installed!")
        self.UpdateSelected = True
        self.FinishUpdate()

    def SkipUpdate(self):
        self.FinishUpdate()
        self.UpdateSelected = True

    def FinishUpdate(self):
        self.Status[0] = True
        self.Frames.Update.destroy()

    ### Launch
    def InitLaunch(self):
        self.ws.title(f"pyLaunch - Launch")
        self.Launch = Launcher()
        self.Frames.Launch = tk.Frame(self.Frames.Body, background=s.FRAME_BG)
        self.Frames.Launch.pack(fill='both', side='top', expand='True')
        if not self.Launch.Initialize():
            self.LaunchLoop()
            return False
        self.StatusLabel.config(text=f"Found Python {config.CONFIGURATION['Setup']['PythonVersion']}. Starting Setup...")
        self.StatusLabel.pack(pady=20)
        self.FinishLaunch()
        return True

    def LaunchLoop(self):
        self.Frames.Launch_Failure = tk.Frame(self.Frames.Launch, background=s.FRAME_BG)
        self.Frames.Launch_Failure.grid_propagate(0)
        self.Frames.Launch_Failure.pack(fill='both', side='left', expand='True')
        gh.LargeLabel(self.Frames.Launch_Failure, text=f"Unable to locate Python {config.CONFIGURATION['Setup']['PythonVersion']}", bg=0).pack()
        gh.LargeLabel(self.Frames.Launch_Failure, text=f"Please install Python {config.CONFIGURATION['Setup']['PythonVersion']} and try again", bg=0).pack()
        gh.Button(self.Frames.Launch_Failure, text="Downloads page", command=lambda: webbrowser.open("https://www.python.org/downloads/")).pack()

        while True:
            pass

    def FinishLaunch(self):
        self.Status[1] = True
        self.Frames.Launch.destroy()

    ### Setup
    def InitSetup(self):
        self.ws.title(f"pyLaunch - Setup")
        self.Setup = Setup(self.Launch.PyPath)
        self.Frames.Setup = tk.Frame(self.Frames.Body, background=s.FRAME_BG)
        self.Frames.Setup.pack_propagate(0)
        self.Frames.Setup.pack(fill='both', side='left', expand='True')
        self.MissingPackages = self.Setup.GetRequired()

        if len(self.MissingPackages) == 0:
            self.StatusLabel.config(text=f"All required packages are installed")
            self.Status[2] = True
            self.FinishSetup()
            return True
        else:
            if len(self.MissingPackages) == 1:
                self.StatusLabel.config(text=f"{len(self.MissingPackages)} package needs to be installed")
            else:
                self.StatusLabel.config(text=f"{len(self.MissingPackages)} packages need to be installed")

        self.Setup.UpdatePip()
        self.PackageIndex = 0
        return self.PackageLoop()
        
    def PackageLoop(self):
        self.DrawPackage()
        while self.PackageIndex < len(self.MissingPackages):
            pass
        self.FinishSetup()
        return True

    def DrawPackage(self):
        package = self.MissingPackages[self.PackageIndex]

        self.Frames.Setup_Install = tk.Frame(self.Frames.Setup, background=s.FRAME_BG)
        self.Frames.Setup_Install.pack_propagate(0)
        self.Frames.Setup_Install.pack(fill='both', side='left', expand='True')
        gh.LargeLabel(self.Frames.Setup_Install, text=f"Install {package[0]}?", bg=0).pack()

        self.Frames.Setup_Install_Buttons = tk.Frame(self.Frames.Setup_Install, background=s.FRAME_BG)
        self.Frames.Setup_Install_Buttons.grid_propagate(0)
        self.Frames.Setup_Install_Buttons.pack(fill='both', side='left', expand='True')
        gh.Button(self.Frames.Setup_Install_Buttons, text="Yes", font=s.FONT_TEXT_LARGE, command=lambda: self.InstallPackage(package[0], package[1])).place(relx=0.25, rely=0.2, anchor='center')
        gh.Button(self.Frames.Setup_Install_Buttons, text="No", font=s.FONT_TEXT_LARGE, command=self.SkipPackage).place(relx=0.75, rely=0.2, anchor='center')

    def InstallPackage(self, pypi, imp):
        self.StatusLabel.config(text=f"Installing {pypi}")
        if not self.Setup.InstallPackage(pypi, imp):
            self.SkipPackage()
        self.Frames.Setup_Install.destroy()
        if self.PackageIndex < len(self.MissingPackages) - 1:
            remaining = len(self.MissingPackages) - self.PackageIndex
            if remaining == 1:
                self.StatusLabel.configure(text=f"{remaining} package needs to be installed")
            else:
                self.StatusLabel.configure(text=f"{remaining} packages need to be installed")
            self.PackageIndex += 1
            self.DrawPackage()
        else:
            self.Status[2] = True
            self.PackageIndex += 1

    def SkipPackage(self) -> bool:
        self.StatusLabel.config(text=f"All packages are required.")
        self.Frames.Setup_Install.destroy()
        self.PackageIndex = len(self.MissingPackages)
        self.FinishSetup()

    def FinishSetup(self):
        self.Frames.Setup.destroy()

if __name__ == "__main__":
    gui = GUI()
    gui.Initialize()