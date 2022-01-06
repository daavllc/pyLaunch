######################################################################################################
#   __        _____        __     __     __    __     ______     __      __    _______    _______    #
#  |  |      /  _  \      |  |   |  |   |  \  |  |   /  __  \   |  |    |  |  |   ____|  |   __  \   #
#  |  |     /  / \  \     |  |   |  |   |   \ |  |  /  /  \__\  |  |    |  |  |  |       |  |  \  \  #
#  |  |    /  /   \  \    |  |   |  |   |    \|  | |  |         |  |____|  |  |  |__     |  |__/  /  #
#  |  |   /  /_____\  \   |  |   |  |   |  |  \  | |  |         |   ____   |  |   __|    |   __  \   #
#  |  |  /  _________  \  |  |   |  |   |  |\    | |  |    ___  |  |    |  |  |  |       |  |  |  |  #
#  |  |_/__/_        \  \  \  \_/   \   |  | \   |  \  \__/  /  |  |    |  |  |  |____   |  |  |  |  #
#  |_________|        \__\  \_____/\_\  |__|  \__|   \______/   |__|    |__|  |_______|  |__|  |__|  #
#                                                                                                    #
######################################################################################################
# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python (3.6+ due to f-strings)
# License: MIT
## Launcher
# Python project setup, updater, and launcher
# Copyright (C) 2022  DAAV, LLC
##########################################################
# Project Lead: Anonoei (https://github.com/Anonoei)

# This file is inteneded to be used as a git submodule in the root of your GitHub project
# If this is placed in a subfoldder of your project, please use the argument "-ap" to specifiy how many directories to go up, ie: ../..
# This file should be launched first, and it will automatically launch your project once configured

import argparse
import os
import sys

import config
from configurator.configurator import Configurator

from user.gui import GUI
from user.cui import CUI
from colors import Colors

def main():
    parser = argparse.ArgumentParser(add_help=True, description="Python project setup, updater, and launcher")
    parser.add_argument("-m", "--modify", dest="Modify", help="modify configuration", action='store_true')
    parser.add_argument("-H", "--hide", dest="Hide", help="Hide Launcher splash screen", action='store_true')
    parser.add_argument("-p", "--path", dest="Path", help="relative path to launcher configuration from this file")
    parser.add_argument("-ap", "--apppath", dest="AppPath", help="relative path to your application from this file")
    parser.add_argument("-UI", "--userinterface", dest="ProjectUI", help="interface launcher will use to launch your project", choices=['CUI', 'GUI'], default='GUI')
    parser.add_argument("-t", "--theme", dest="Theme", help="color theme for user gui", choices=['dark', 'light'], default='dark')
    parser.add_argument("-LUI", "--launcheruserinterface", dest="LauncherUI", help="interface for Launcher configuration", choices=['CUI', 'GUI'], default='GUI')
    args = parser.parse_args()
    if not args.Hide:
        print("   __        _____        __     __     __    __     ______     __      __    _______    _______    ")
        print("  |  |      /  _  \      |  |   |  |   |  \  |  |   /  __  \   |  |    |  |  |   ____|  |   __  \   ")
        print("  |  |     /  / \  \     |  |   |  |   |   \ |  |  /  /  \__\  |  |    |  |  |  |       |  |  \  \  ")
        print("  |  |    /  /   \  \    |  |   |  |   |    \|  | |  |         |  |____|  |  |  |__     |  |__/  /  ")
        print("  |  |   /  /_____\  \   |  |   |  |   |  |  \  | |  |         |   ____   |  |   __|    |   __  \   ")
        print("  |  |  /  _________  \  |  |   |  |   |  |\    | |  |    ___  |  |    |  |  |  |       |  |  |  |  ")
        print("  |  |_/__/_        \  \  \  \_/   \   |  | \   |  \  \__/  /  |  |    |  |  |  |____   |  |  |  |  ")
        print("  |_________|        \__\  \_____/\_\  |__|  \__|   \______/   |__|    |__|  |_______|  |__|  |__|  ")
        print(f" Copyright ©2022 DAAV, LLC - Version {config.VERSION}\n")

    # Setup paths
    config.PATH_ROOT = os.path.abspath(".")
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

    # Theme
    Colors.Get().Set(args.Theme)

    cfgr = Configurator()
    if os.path.exists(f"{config.PATH_ROOT}{os.sep}{config.FILE_USERCONFIG}") and not args.Modify:
        cfgr.Load()
        if cfgr.Configuration['Version'] == config.VERSION_CONFIGURATION:
            LaunchConfiguration(cfgr, args) # Configuration is up to date, good-to-go
    NewConfiguration(cfgr, args)

def NewConfiguration(cfgr, args):
    if not cfgr.New(args.LauncherUI):
        print("You didn't finish configuration")
        input("Press enter to exit")
        sys.exit(0)
    cfgr.Load()
    LaunchConfiguration(cfgr, args)
    

def LaunchConfiguration(cfgr, args):
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