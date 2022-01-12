# pyLaunch
 Python project setup, updater, and launcher

## Purpose:
Increase project productivity and provide features easily. Once installed as a git submodule (or downloaded), placed in a project and configured, it automatically provides updates, dependency installation, and launcher. It automatically finds the required version of python, launches projects with it. In addition, pyLaunch:Launch allows custom exit values, which can be used to reload source code quickly and enable easier code editing.

## Details:
 - Project lead: [Anonoei](https://github.com/Anonoei)
 - Langauge: Python 3.6+ (due to f-strings, tested on 3.10)
 - License: MIT
 - Dependancies: None
 - Documentation: [docs.daav.us](https://docs.daav.us/pyLaunch)

----

## Current status/roadmap:
 - [X] Documentation
   - [X] In-depth documentation at [docs.daav.us/pyLaunch](https://docs.daav.us/pyLaunch)
   - [X] Basic overview/help (CUI/GUI)
 - [X] Frontend UI
   - [X] [CUI](https://github.com/daavofficial/pyLaunch/blob/main/frontend/cui.py)
     - [X] Update/Launch/Setup
   - [X] [GUI](https://github.com/daavofficial/pyLaunch/blob/main/frontend/cui.py)
     - [X] Color Themes
     - [X] Update/Launch/Setup
 - [X] Configurator UI
   - [ ] Modify previous configuration
   - [X] Better input protection
   - [X] [CUI](https://github.com/daavofficial/pyLaunch/blob/main/configurator/cui.py)
     - [X] Color Themes
     - [X] Provide help for formatting
     - [X] Modify all configuration options
   - [X] [GUI](https://github.com/daavofficial/pyLaunch/blob/main/configurator/gui.py)
     - [X] Themes/color schemes (dark/light)
     - [X] Modify all configuration options
 - [ ] Pull private repositories
 - [X] Arguments
 - [X] Saveable configurations

----

## File Structure
 - userconfig.json (stores configuration for project)
 - confpath.txt (stores relative path to userconfig)

## Configuration

### [Setup](https://github.com/daavofficial/pyLaunch/blob/main/frontend/setup.py)
 - Automatic dependancy installation
 - Variables:
   - Python Version
   - Minimum Python Version
   - Python Folder (Internal)
   - Packages (list of required packages, used as pypiName:importName [ex: pyyaml:yaml])
  
### [Update](https://github.com/daavofficial/pyLaunch/blob/main/frontend/update.py)
 - Automatic update checking, downloading and installing
 - Variables:
   - Organization
   - Repository
   - Branch
   - VersionPath (Project path to file containing version [ex: /config.py])
   - Find (Line to grab from VersionPath [ex: VERSION = ])
   - Token (GitHub token for private repositories)
   - Skip Checking for updates

### [Launch](https://github.com/daavofficial/pyLaunch/blob/main/frontend/launch.py)
 - Locates required Python version, and provides custom error catching, allowing project reloading for faster development, or launching with arguments
 - Variables:
   - Project Root (Relative path to project root [ex: ..])
   - Project Main (project path to the 'main' file [ex: /start.py])
   - Error Codes (list of error codes, used as code:argument [ex: -2:-UI GUI])
   - Skip error code checking

----

## Installation
 - GitHub project
   1. Open git terminal in your repository folder
   2. Run `git submodule add https://github.com/daavofficial/pyLaunch.git`
   3. Open the new `pyLaunch` folder
   4. Launch
      - Run [start.py](https://github.com/daavofficial/pyLaunch/blob/main/start.py)
      - Double Click [example-launch-gui.bat](https://github.com/daavofficial/pyLaunch/blob/main/example-launch-gui.bat) (Windows)
   5. Configure, by following the prompts provided

## Download from source
 1. `git clone https://github.com/daavofficial/pyLaunch.git`
 3. Open 'pyLaunch' folder.
 4. Run [start.py](https://github.com/daavofficial/pyLaunch/blob/main/start.py) or use an example-launch file

## License
Copyright © 2022 DAAV, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
