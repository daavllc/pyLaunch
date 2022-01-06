import asyncio
import tkinter as tk
from tkinter import ttk
import time
import threading
import webbrowser

import config
from colors import Colors

from user.update import Update
from user.launch import Launch
from user.setup import Setup

c = Colors.Get()

class GUI:
    class _Storage:
        pass

    def Start(self):
        self.Initialize()
        self.Automatic()
    
    def Initialize(self):
        self.ws = tk.Tk()
        self.ws.title(f"Launcher")
        self.ws.geometry("400x300")
        self.ws.resizable(width=False, height=False)
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
        thread = threading.Thread(target=self.CreateThread)
        thread.start()
        self.ws.mainloop()
        if self.Status[0] and self.Status[1] and self.Status[2]:
            print("Launching!")
            self.Launch.Launcher()
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
        while time.perf_counter() - StartTime < 1.0:
            pass
        self.InitUpdate()
        if self.InitLaunch():
            self.InitSetup()
        self.ws.destroy()

    ### Update
    def InitUpdate(self) -> bool:
        self.ws.title(f"Launcher - Update")
        self.Update = Update()
        self.Frames.Update = tk.Frame(self.ws, background=c.FRAME_BG2)
        self.Frames.Update.pack_propagate(0)
        self.Frames.Update.pack(fill='both', side='left', expand='True')
        if not self.Update.CheckConnection():
            tk.Label(self.Frames.Update, text="Unable to connect to the internet", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG).pack()
            self.Frames.Update.destroy()
            self.Status[0] = True
            return True
        self.StatusLabel = tk.Label(self.Frames.Update, text="Checking for update...", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG)
        self.StatusLabel.pack(pady=20)

        if self.Update.Check():
            self.StatusLabel.config(text="An update is available")
        else:
            self.StatusLabel.config(text="You have the latest version")
            self.Frames.Update.destroy()
            self.Status[0] = True
            return True

        self.Frames.Update_Available = tk.Frame(self.Frames.Update, background=c.FRAME_BG2)
        self.Frames.Update_Available.grid_propagate(0)
        self.Frames.Update_Available.pack(fill='both', side='left', expand='False')
        tk.Label(self.Frames.Update_Available, text=f"Update from [v{'.'.join(self.Update.Versions[0])}] to [v{'.'.join(self.Update.Versions[1])}]?", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG).grid(row=0)
        tk.Button(self.Frames.Update_Available, text="Yes", callback=self.InstallUpdate).grid(column=0, row=1)
        tk.Button(self.Frames.Update_Available, text="No", callback=self.SkipUpdate).grid(column=1, row=1)

    def InstallUpdate(self):
        self.Frames.Update_Available.destroy()
        self.StatusLabel.config(text="Downloading update...")
        if not self.Update.DownloadUpdate():
            self.StatusLabel.config(text="Failed to download update")
        else:
            self.StatusLabel.config(text="Complete! Installing...")

        if not self.Update.InstallUpdate():
            self.StatusLabel.config(text="Failed to install update")
        else:
            self.StatusLabel.config(text="Update installed!")
        self.Frames.Update.destroy()
        self.Status[0] = True

    def SkipUpdate(self):
        self.Frames.Update_Available.destroy()
        self.Frames.Update.destroy()
        self.Status[0] = True

    ### Launch
    def InitLaunch(self):
        self.ws.title(f"Launcher - Launch")
        self.Launch = Launch()
        self.Frames.Launch = tk.Frame(self.ws, background=c.FRAME_BG2)
        self.Frames.Launch.pack_propagate(0)
        self.Frames.Launch.pack(fill='both', side='left', expand='True')
        if not self.Launch.Initialize():
            self.Frames.Launch_Failure = tk.Frame(self.Frames.Launch, background=c.FRAME_BG2)
            self.Frames.Launch_Failure.grid_propagate(0)
            self.Frames.Launch_Failure.pack(fill='both', side='left', expand='True')
            tk.Label(self.Frames.Launch_Failure, text=f"Unable to locate Python {config.USER_CONFIGURATION['Setup']['PythonVersion']}", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG).pack()
            tk.Label(self.Frames.Launch_Failure, text=f"Please install Python {config.USER_CONFIGURATION['Setup']['PythonVersion']} and try again", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG).pack()
            tk.Button(self.Frames.Launch_Failure, text="Downloads page", callback=lambda: webbrowser.open("https://www.python.org/downloads/")).pack()
            return False
        self.StatusLabel = tk.Label(self.Frames.Launch, text=f"Found Python {config.USER_CONFIGURATION['Setup']['PythonVersion']}. Starting Setup...", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG)
        self.StatusLabel.pack(pady=20)
        self.Frames.Launch.destroy()
        self.Status[1] = True
        return True

    ### Setup
    def InitSetup(self):
        self.ws.title(f"Launcher - Setup")
        self.Setup = Setup(self.Launch.PyPath)
        self.Frames.Setup = tk.Frame(self.ws, background=c.FRAME_BG2)
        self.Frames.Setup.pack_propagate(0)
        self.Frames.Setup.pack(fill='both', side='left', expand='True')
        self.MissingPackages = self.Setup.GetRequired()

        if len(self.MissingPackages) == 0:
            self.StatusLabel = tk.Label(self.Frames.Setup, text=f"All required packages are installed", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG)
            self.StatusLabel.pack(pady=20)
            self.Status[2] = True
            return True
        else:
            if len(self.MissingPackages) == 1:
                self.StatusLabel = tk.Label(self.Frames.Setup, text=f"{len(self.MissingPackages)} package needs to be installed", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG)
            else:
                self.StatusLabel = tk.Label(self.Frames.Setup, text=f"{len(self.MissingPackages)} packages need to be installed", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG)
            self.StatusLabel.pack(pady=20)
        self.Setup.UpdatePip()
        self.PackageIndex = 0
        self.PackageLoop()
        
    def PackageLoop(self):
        self.DrawPackage()
        while self.PackageIndex < len(self.MissingPackages):
            pass
        self.FinishSetup()

    def DrawPackage(self):
        package = self.MissingPackages[self.PackageIndex]

        self.Frames.Setup_Install = tk.Frame(self.Frames.Setup, background=c.FRAME_BG2)
        self.Frames.Setup_Install.pack_propagate(0)
        self.Frames.Setup_Install.pack(fill='both', side='left', expand='True')
        tk.Label(self.Frames.Setup_Install, text=f"Install {package[0]}?", font=14, background=c.FRAME_BG2, foreground=c.LABEL_FG).pack()

        self.Frames.Setup_Install_Buttons = tk.Frame(self.Frames.Setup_Install, background=c.FRAME_BG2)
        self.Frames.Setup_Install_Buttons.grid_propagate(0)
        self.Frames.Setup_Install_Buttons.pack(fill='both', side='left', expand='True')
        tk.Button(self.Frames.Setup_Install_Buttons, text="Yes", font=18, command=lambda: self.InstallPackage(package[0], package[1])).place(relx=0.25, rely=0.2, anchor='center')
        tk.Button(self.Frames.Setup_Install_Buttons, text="No", font=18, command=self.SkipPackage).place(relx=0.75, rely=0.2, anchor='center')

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

    ### Launch Project
    def Success(self):
        self.ws.destroy()

    def Failure(self):
        self.ws.destroy()

if __name__ == "__main__":
    gui = GUI()
    gui.Initialize()