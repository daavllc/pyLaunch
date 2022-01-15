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
 - [ ] Language Support
    - [ ] C++
    - [X] Python
 - [ ] Pull private repositories
 - [X] Arguments
 - [X] Saveable configurations

----

## Using pyLaunch
 1. Download/place in your project's root directory
    - Git submodule
      1. Open git terminal in your repository folder
      2. Run `git submodule add https://github.com/daavofficial/pyLaunch.git`
    - Manual
      1. Click the 'Code' button near the top right corner > Download ZIP
      2. Extract the zip file
      3. Move the `pyLaunch` folder into your project's root directory
 2. Create your project's launch script
      - Example (Windows)
        - Right Click > New > Text Document and add the following:
          - `@echo off`
          - `python "pyLaunch/start.py`
        - File > Save As
        - Save as type: `All Files`
        - File name: `start.bat` or whatever you want to name it, with the .bat extension
 3. Launch the new `start` script
 4. Configure your project with pyLaunch's Configurator
 5. Update your project's .gitignore
    - Add the following to your .gitignore file
    - `pyLaunch/logs`

## Contributing to pyLaunch
 1. Download from source
    - `git clone https://github.com/daavofficial/pyLaunch.git`
    - 'Code' button near the top right > Download ZIP, extract the file
 3. Open 'pyLaunch' folder.
 4. Have fun! Read our [documentation](https://docs.daav.us/pyLaunch) for more under-the-hood details

## License
Copyright © 2022 DAAV, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
