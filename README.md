# Launcher
 Python project setup, updater, and launcher

## Purpose:
Increase project productivity and provide features easily. Once installed as a git submodule (or downloaded), placed in a project and configured, it automatically provides updates, dependancy installation, and launcher. It automatically finds the required version of python, launches projects with it. In addition, Launcher:Launch allows custom exit values, which can be used to reload source code quickly and enable easier code editing.

## Details:
 - Project lead: [Anonoei](https://github.com/Anonoei)
 - Langauge: Python 3.6+ (due to f-strings, tested on 3.10)
 - License: MIT
 - Dependancies: None

----

## Current status/roadmap:
 - [X] Documentation
   - [X] Basic overview/help (CUI/GUI)
 - [X] End-user UI
   - [X] CUI
     - [X] Update/Launch/Setup
   - [X] GUI
     - [X] Update/Launch/Setup
 - [X] Launcher UI
   - [ ] Better input protection
   - [X] CUI
     - [X] Provide help for formatting
     - [X] Modify all configuration options
   - [X] GUI
     - [X] Themes/color schemes (dark/light)
     - [X] Modify all configuration options
 - [X] Arguments
 - [X] Saveable configurations

----

## File Structure
 - userconfig.json (stores configuration for project)
 - confpath.txt (stores relative path to userconfig)

## Configuration

### [Setup](https://github.com/daavofficial/Launcher/blob/main/user/setup.py)
 - Automatic dependancy installation
 - Variables:
   - PythonVersion (Required Python Version [ex: 3.10])
   - PythonFolder (Internal)
   - Packages (list of required packages, used as pypiName:importName [ex: pyyaml:yaml])
  
### [Update](https://github.com/daavofficial/Launcher/blob/main/user/update.py)
 - Automatic update checking, downloading and installing
 - Variables:
   - Organization (GitHub organization/user [ex: daavofficial])
   - Repository (Repository Name [ex: Launcher])
   - Branch ([ex: main])
   - VersionPath (Project path to file containing version [ex: /config.py])
   - Find (Line to grab from VersionPath [ex: VERSION = ])
   - Token (GitHub token for private repositories)

### [Launch](https://github.com/daavofficial/Launcher/blob/main/user/launch.py)
 - Locates required Python version, and provides custom error catching, allowing project reloading for faster development, or launching with arguments
 - Variables:
   - ProjectRoot (Relative path to project root [ex: ..])
   - ProjectMain (project path to the 'main' file [ex: /start.py])

----

## Installation
 - GitHub project
   1. Open git terminal in your repository folder
   2. Run `git submodule add https://github.com/daavofficial/Launcher.git`
   3. Open the new `Launcher` folder
   4. Launch
      - Run [start.py](https://github.com/daavofficial/Launcher/blob/main/start.py)
      - Double Click [example-launch-gui.bat](https://github.com/daavofficial/Launcher/blob/main/example-launch-gui.bat) (Windows)
   5. Configure, by following the prompts provided

## Download from source
 1. `git clone https://github.com/daavofficial/Launcher.git`
 3. Open 'Launcher' folder.
 4. Run [start.py](https://github.com/daavofficial/Launcher/blob/main/start.py) or use an example-launch file

## License
Copyright © 2022 DAAV, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
