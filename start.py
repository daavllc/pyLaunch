# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python (3.6+ due to f-strings)
# License: MIT
## pyLaunch
# Python project setup, updater, and pyLaunch
# Copyright (C) 2022  DAAV, LLC
##########################################################
# Project Lead: Anonoei (https://github.com/Anonoei)

# This file is inteneded to be used as a git submodule in the root of your GitHub project
# If this is placed in a subfoldder of your project, please use the argument "-ap" to specifiy how many directories to go up, ie: ../..
# This file should be launched first, and it will automatically launch your project once configured

import argparse
import os
import sys
import platform
import shutil
import urllib.request

import helpers.config as config
from configurator.configurator import Configurator

from frontend.gui import GUI
from frontend.cui import CUI
from helpers.style import Style
from helpers.logger import Logger

log = None

def main():
    global log
    s = Style.Get()
    parser = argparse.ArgumentParser(add_help=True, description="Python project setup, updater, and pyLaunch")
    parser.add_argument("-H", "--hide", dest="Hide", help="don't show pyLaunch splash screen", action='store_true')
    parser.add_argument("-l", "--loglevel", dest="LogLevel", help="log level for printing and writing to file [default=info]", choices=['debug', 'info', 'warn', 'error', 'critical', 'none'], default='info')
    parser.add_argument("-W", "--logwrite", dest="LogWrite", help="skip writing logs to file", action='store_true')
    parser.add_argument("-P", "--logprint", dest="LogPrint", help="skip printing logs to console", action='store_true')
    parser.add_argument("-u", "--update", dest="Update", help="check for update", action='store_true')
    parser.add_argument("-UI", "--user-interface", dest="UI", help="interface for pyLaunch launcher", choices=['CUI', 'GUI'], default='GUI')
    parser.add_argument("-t", "--theme", dest="Theme", help="color theme for GUI [default=dark]", choices=s.GetThemes(), default='dark')

    configurator = parser.add_argument_group("configurator", "configurator arguments")
    configurator.add_argument("-R", "--reset", dest="Reset", help="clear logs and configuration", action='store_true')
    configurator.add_argument("-m", "--modify", dest="Modify", help="modify configuration", action='store_true')
    configurator.add_argument("-s", "--skip", dest="Skip", help="skip checking configuration version", action='store_true')
    configurator.add_argument("-CI", "--interface", dest="CI", help="interface for pyLaunch configurator [default=GUI]", choices=['CUI', 'GUI'], default='GUI')

    counter = parser.add_argument_group("counter", "recursivly count a folder's files with extention")
    counter.add_argument("-c", "--count", dest="Count", help="enable counter, show lines and files", action='store_true')
    counter.add_argument("-cn", "--counter-name", dest="CtrName", help="name of project [ex: pyLauncher]")
    counter.add_argument("-cp", "--counter-path", dest="CtrPath", help="relative path to project [ex: ..]")
    counter.add_argument("-cx", "--counter-extentions", dest="CtrExtensions", help="count files with these extensions [ex: .py,.bat]")

    args = parser.parse_args()
    config.LOG_CONF = dict(level = args.LogLevel, print = not args.LogPrint, write = not args.LogWrite)
    log = Logger("pyLaunch", "pyLaunch.log")
    if not args.Hide:
        print("                 __                           __  ")
        print("    ____  __  __/ /   ____ ___  ______  _____/ /_ ")
        print("   / __ \/ / / / /   / __ `/ / / / __ \/ ___/ __ \\")
        print("  / /_/ / /_/ / /___/ /_/ / /_/ / / / / /__/ / / /")
        print(" / .___/\__, /_____/\__,_/\__,_/_/ /_/\___/_/ /_/ ")
        print("/_/    /____/                                     ")
        print("                                                  ")
        print(f" Copyright ©2022 DAAV, LLC - Version {config.VERSION}")
        print(f" Licensed under the MIT license. See LICENSE for details.\n")

    # Setup paths
    config.PATH_ROOT = os.path.abspath(".")
    if not config.PATH_ROOT.split(os.sep)[-1] == "pyLaunch":
        if os.path.exists(f"{config.PATH_ROOT}{os.sep}pyLaunch"):
            config.PATH_ROOT = f"{config.PATH_ROOT}{os.sep}pyLaunch"
            os.chdir(config.PATH_ROOT)
        else:
            print("Unable to locate pyLaunch directory.")
            input("Press enter to exit...")
            sys.exit(0)

    if not os.path.exists("logs"):
        os.mkdir("logs")
    log.debug(f"{config.PATH_ROOT = }")
    log.debug(f"Launching with {platform.platform()} on {platform.machine()}")
    if sys.version is not None:
        log.debug(f"Using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    config.PATH_USERCONFIG = config.PATH_ROOT
    with open("confpath.txt", "w", encoding="utf-8") as f:
        f.write(config.FILE_USERCONFIG + "\n")

    if args.Update:
        log.info(f"Checking for update")
        CheckedVersion = None
        try:
            response = urllib.request.urlopen(f"https://raw.githubusercontent.com/daavofficial/pyLaunch/main/helpers/config.py")
            content = response.read().decode("UTF-8").split("\n")
            for line in content:
                if "VERSION = " in line:
                    CheckedVersion = line[len("VERSION = "):].replace('"', "")
        except urllib.error.HTTPError as e:
            print(f"Unable to check for version: {e}")
            input("Press enter to exit")
            sys.exit(0)
        
        cVer = CheckedVersion.split(".")
        iVer = config.VERSION.split(".")
        for installed, checked in zip(iVer, cVer):
            installed = int(installed)
            checked = int(checked)
            val = checked - installed
            if val < 0:
                print(f"Local version greater than public version - [{config.VERSION}/{CheckedVersion}]")
                break
            elif val > 0:
                print(f"An update is available [{config.VERSION}/{CheckedVersion}]")
                break
        else:
            print(f"Up to date! [{config.VERSION}]")
        input("Press enter to exit")
        sys.exit(0)

    if args.Count:
        from helpers.count import Counter as Counter
        print(f"{args.CtrName = } {args.CtrPath = } {args.CtrExtensions = }")
        if args.CtrName is None and args.CtrPath is None and args.CtrExtensions is None:
            counter = Counter([".py"], "PyLaunch", ".")
            counter.Count()
            counter.Print()
        elif (args.CtrName is not None) and (args.CtrPath is not None) and (args.CtrExtensions is not None):
            counter = Counter(args.CtrExtensions.split(","), args.CtrName, args.CtrPath)
            counter.Count()
            counter.Print()
        else:
            print("-cn, -cp and -cx are all required arguments. ")
           
        input("Press enter to exit")
        sys.exit(0)

    if args.Reset:
        Reset()

    # Theme
    s.Set(args.Theme)

    cfgr = Configurator.Get()
    if args.Modify:
        log.debug("Creating new configuration due to modify argument")
        if os.path.exists(f"{config.PATH_ROOT}{os.sep}{config.FILE_USERCONFIG}"):
            cfgr.Load()
        NewConfiguration(cfgr, args)
    if not os.path.exists(f"{config.PATH_ROOT}{os.sep}{config.FILE_USERCONFIG}"):
        log.debug("Configuration file not found, creating new")
        NewConfiguration(cfgr, args)
    
    cfgr.Load()
    if cfgr.Configuration.data['Version'] == config.VERSION_CONFIGURATION or args.Skip:
        log.debug(f"Found current configuration [{config.VERSION_CONFIGURATION}]")
        LaunchConfiguration(cfgr, args) # Configuration is up to date, good-to-go
    else:
        log.debug(f"Found out of date configuration: [{cfgr.Configuration.data['Version']}/{config.VERSION_CONFIGURATION}]")
        NewConfiguration(cfgr, args)

def NewConfiguration(cfgr, args):
    if not cfgr.New(args.CI):
        log.warn("Configuration incomplete, aborting...")
        input("Press enter to exit")
        sys.exit(0)
    cfgr.Load()
    LaunchConfiguration(cfgr, args)
    

def LaunchConfiguration(cfgr, args):
    log.info("Launching configuration")
    config.USER_CONFIGURATION = cfgr.Configuration
    ui = None
    if args.UI == "GUI":
        ui = GUI()
    else:
        ui = CUI()
    ui.Start()
    sys.exit(0)

def Reset():
    if os.path.exists("confpath.txt"):
        with open("confpath.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            lines = lines[0].strip()
            if os.name == "nt":
                lines = lines.replace('\\', '/')
            if os.path.exists(lines):
                os.remove(lines)
                print(f"Deleted: {config.FILE_USERCONFIG}")
        os.remove("confpath.txt")
        print(f"Deleted: confpath.txt")
    elif os.path.exists(config.FILE_USERCONFIG):
        os.remove(config.FILE_USERCONFIG)
        print(f"Deleted: {config.FILE_USERCONFIG}")

    shutil.rmtree("logs")
    print(f"Deleted: logs")
    log.info("Successfully reset!")
    if 'n' in input("Start normally? (Y/n) > "):
        sys.exit(0)

if __name__ == "__main__":
    main()
else:
    print("This program is only intended to be run directly")
    input("Press enter to exit")
    sys.exit(0)