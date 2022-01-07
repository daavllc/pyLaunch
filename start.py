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

import helpers.config as config
from configurator.configurator import Configurator

from user.gui import GUI
from user.cui import CUI
from helpers.style import Style
from helpers.logger import Logger

log = None

def main():
    global log
    s = Style.Get()
    parser = argparse.ArgumentParser(add_help=True, description="Python project setup, updater, and pyLaunch")
    parser.add_argument("-m", "--modify", dest="Modify", help="modify configuration", action='store_true')
    parser.add_argument("-H", "--hide", dest="Hide", help="Hide pyLaunch splash screen", action='store_true')
    parser.add_argument("-p", "--path", dest="Path", help="relative path to pyLaunch configuration from this file")
    parser.add_argument("-ap", "--apppath", dest="AppPath", help="relative path to your application from this file")
    parser.add_argument("-UI", "--userinterface", dest="ProjectUI", help="interface pyLaunch will use to launch your project", choices=['CUI', 'GUI'], default='GUI')
    parser.add_argument("-t", "--theme", dest="Theme", help="color theme for user gui", choices=s.GetThemes(), default='dark')
    parser.add_argument("-LUI", "--pyLaunchuserinterface", dest="pyLaunchUI", help="interface for pyLaunch configuration", choices=['CUI', 'GUI'], default='GUI')
    parser.add_argument("-l", "--loglevel", dest="LogLevel", help="log level for printing and writing to file", choices=['none', 'debug', 'info', 'warn', 'error', 'critical'], default='debug')
    parser.add_argument("-P", "--logprint", dest="LogPrint", help="skip printing logs to console", action='store_true')
    parser.add_argument("-W", "--logwrite", dest="LogWrite", help="skip writing logs to file", action='store_true')
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
        print(f" Copyright ©2022 DAAV, LLC - Version {config.VERSION}\n")

    # Setup paths
    config.PATH_ROOT = os.path.abspath(".")
    log.debug(f"Using PATH_ROOT: {config.PATH_ROOT}")
    if args.Path:
        config.PATH_USERCONFIG = args.Path
        with open("confpath.txt", "w", encoding="utf-8") as f:
            if os.name == "nt":
                f.write(config.PATH_USERCONFIG.replace('\\', '/') + "/" + config.FILE_USERCONFIG + "\n")
            else:
                f.write(f"{config.PATH_USERCONFIG}/{config.FILE_USERCONFIG}" + "\n")
    else:
        config.PATH_USERCONFIG = config.PATH_ROOT
        with open("confpath.txt", "w", encoding="utf-8") as f:
            f.write(config.FILE_USERCONFIG + "\n")

    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Theme
    s.Set(args.Theme)

    cfgr = Configurator()
    if args.Modify:
        log.debug("Creating new configuration due to modify argument")
        NewConfiguration(cfgr, args)
    if not os.path.exists(f"{config.PATH_ROOT}{os.sep}{config.FILE_USERCONFIG}"):
        print("unexist")
        NewConfiguration(cfgr, args)
    
    cfgr.Load()
    if cfgr.Configuration.data['Version'] == config.VERSION_CONFIGURATION:
        log.debug(f"Found current configuration [{config.VERSION_CONFIGURATION}]")
        LaunchConfiguration(cfgr, args) # Configuration is up to date, good-to-go
    else:
        log.debug(f"Found out of date configuration: [{cfgr.Configuration.data['Version']}/{config.VERSION_CONFIGURATION}]")
        NewConfiguration(cfgr, args)

def NewConfiguration(cfgr, args):
    if not cfgr.New(args.pyLaunchUI):
        log.warn("Configuration incomplete, aborting...")
        input("Press enter to exit")
        sys.exit(0)
    cfgr.Load()
    LaunchConfiguration(cfgr, args)
    

def LaunchConfiguration(cfgr, args):
    log.info("Launching configuration")
    config.USER_CONFIGURATION = cfgr.Configuration
    ui = None
    if args.ProjectUI == "GUI":
        ui = GUI()
    else:
        ui = CUI()
    ui.Start()
    sys.exit(0)

if __name__ == "__main__":
    main()
else:
    print("This program is only intended to be run directly")
    input("Press enter to exit")
    sys.exit(0)