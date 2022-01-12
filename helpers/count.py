import os

class Counter:
    class Info:
        Longest = dict(
            Name = 0, # len of longest name
            Dirs = 0, # len of longest dir
            File = 0, # len of longest file name
            Char = 0, # len of longest char count
            Line = 0, # len of longest line count
            Size = 0  # len of longest size count
        )
        Totals = dict(
            Dirs = 0, # Total number of dirs
            File = 0, # Total number of files
            Char = 0, # Total of all Project chars
            Line = 0, # Total of all Project lines
            Size = 0 # Total of all Project TotalSize
        )
        Dirs = {} # Name: [files: int, chars: int, lines: int, size: int, files {filename : [chars: int, lines: int, size: str]}]

    def __init__(self, SearchFor: list, ProjectName: str, SrcPath: str):
        self.info = self.Info()
        self.SearchFor = SearchFor
        self.ProjectName = ProjectName
        self.SrcPath = os.path.abspath(SrcPath)
        self.Info.Longest['Name'] = len(self.ProjectName)
        if self.ProjectName == 'pyLaunch':
            self.SkipPyLaunch = False
        else:
            self.SkipPyLaunch = True

    def Count(self):
        p = "Counting "
        p += ', '.join(self.SearchFor)
        print(p + " files...")
        self.GetInfo(self.SrcPath)

        if self.Info.Longest['Char'] < len(str(self.Info.Totals['Char'])):
            self.Info.Longest['Char'] = len(str(self.Info.Totals['Char']))

        if self.Info.Longest['Line'] < len(str(self.Info.Totals['Line'])):
            self.Info.Longest['Line'] = len(str(self.Info.Totals['Char']))

        if self.Info.Longest['Size'] < len(self.GetSizeStr(self.Info.Totals['Size'])):
            self.Info.Longest['Size'] = len(self.GetSizeStr(self.Info.Totals['Size']))

    def Print(self):
        columnHeader = ["PROJECT", "DIRS", "FILES", "LINES", "CHARS", "SIZE"]
        if len(columnHeader[0]) > self.Info.Longest['Name']:
            self.Info.Longest['Name'] = len(columnHeader[0])
        if len(columnHeader[1]) > self.Info.Longest['Dirs']:
            self.Info.Longest['Dirs'] = len(columnHeader[1])
        if len(columnHeader[2]) > self.Info.Longest['File']:
            self.Info.Longest['File'] = len(columnHeader[2])
        if len(columnHeader[3]) > self.Info.Longest['Line']:
            self.Info.Longest['Line'] = len(columnHeader[3])
        if len(columnHeader[4]) > self.Info.Longest['Char']:
            self.Info.Longest['Char'] = len(columnHeader[4])
        if len(columnHeader[5]) > self.Info.Longest['Size']:
            self.Info.Longest['Size'] = len(columnHeader[5])

        nameLen = self.Info.Longest['Name']
        dirsLen = self.Info.Longest['Dirs']
        fileLen = self.Info.Longest['File']
        charLen = self.Info.Longest['Char']
        lineLen = self.Info.Longest['Line']
        sizeLen = self.Info.Longest['Size']

        outerSep = " {} | {} | {} | {} | {} | {} |".format(
            self.Center("=", nameLen, "="), self.Center("=", dirsLen, "="),
            self.Center("=", fileLen, "="), self.Center("=", lineLen, "="),
            self.Center("=", charLen, "="), self.Center("=", sizeLen, "=")
        )
        innerSep = " {} | {} | {} | {} | {} | {} |".format(
            self.Center("-", nameLen, "-"), self.Center("-", dirsLen, "-"),
            self.Center("-", fileLen, "-"), self.Center("-", lineLen, "-"),
            self.Center("-", charLen, "-"), self.Center("-", sizeLen, "-")
        )
        bodySep = " {} | {} | {} | {} | {} | {} |".format(
            self.Center(" ", nameLen, " "), self.Center("-", dirsLen, "-"),
            self.Center("-", fileLen, "-"), self.Center("-", lineLen, "-"),
            self.Center("-", charLen, "-"), self.Center("-", sizeLen, "-")
        )
        header = " {} | {} | {} | {} | {} | {} |".format(
            self.Center(columnHeader[0], nameLen), self.Center(columnHeader[1], dirsLen),
            self.Center(columnHeader[2], fileLen), self.Center(columnHeader[3], lineLen),
            self.Center(columnHeader[4], charLen), self.Center(columnHeader[5], sizeLen)
        )
        # columnHeader = ["PROJECT", "DIRS", "FILES", "LINES", "CHARS", "SIZE"]
        print(outerSep)
        print(header)
        print(innerSep)
        # body
        for key, value in self.Info.Dirs.items():
            print(" {} | {} | {} | {} | {} | {} |".format(
                self.Left(" ", nameLen), self.Left(key, dirsLen),
                self.Center(str(value[0]), fileLen), self.Center(str(value[2]), lineLen),
                self.Center(str(value[1]), charLen), self.Right(self.GetSizeStr(value[3]), sizeLen)
            ))
            for key, value in value[4].items():
                print(" {} | {} | {} | {} | {} | {} |".format(
                    self.Left(" ", nameLen), self.Left(" ", dirsLen),
                    self.Left(key, fileLen), self.Left(str(value[1]), lineLen),
                    self.Left(str(value[0]), charLen), self.Right(self.GetSizeStr(value[2]), sizeLen)
                ))
            print(bodySep)

        print(" {} | {} | {} | {} | {} | {} |".format(
            self.Left(self.ProjectName, nameLen), self.Left(str(self.Info.Totals['Dirs']), dirsLen),
            self.Left(str(self.Info.Totals['File']), fileLen), self.Left(str(self.Info.Totals['Line']), lineLen),
            self.Left(str(self.Info.Totals['Char']), charLen), self.Right(self.GetSizeStr(self.Info.Totals['Size']), sizeLen)
        ))
        print(outerSep)

    def GetSizeStr(self, size: int) -> str:
        if size < 1000:
            return "{} B".format(size)
        elif size < 10000000:
            return "{:.2f} KB".format(size / 1000)
        else:
            return "{:.2f} MB".format(size / 10000000)


    def GetInfo(self, path: str):
        if path.endswith(os.sep):
            path = path[:-1]
        for file in os.listdir(path):
            if os.path.isdir(f"{path}{os.sep}{file}"):
                if self.SkipPyLaunch and file == 'pyLaunch':
                    continue
                self.GetInfo(f"{path}{os.sep}{file}")
            else:
                fname, extension = os.path.splitext(f"{path}{os.sep}{file}")
                if extension in self.SearchFor:
                    size = os.path.getsize(f"{path}{os.sep}{file}")
                    chars = None
                    lines = None
                    with open (f"{path}{os.sep}{file}", "r") as f:
                        data = f.read()
                        chars = len(data)
                        lines = len(data.split("\n"))
                    folder = path.split(os.sep)[-1]
                    if self.Info.Dirs.get(folder, None) is None:
                        self.Info.Dirs[folder] = [1, chars, lines, size, {file : [chars, lines, size]}]
                        self.Info.Totals['Dirs'] += 1
                    else:
                        self.Info.Dirs[folder][0] += 1
                        self.Info.Dirs[folder][1] += chars
                        self.Info.Dirs[folder][2] += lines
                        self.Info.Dirs[folder][3] += size
                        self.Info.Dirs[folder][4][file] = [chars, lines, size]

                    self.Info.Totals['File'] += 1
                    self.Info.Totals['Char'] += chars
                    self.Info.Totals['Line'] += lines
                    self.Info.Totals['Size'] += size

                    if self.Info.Longest['Dirs'] < len(folder):
                        self.Info.Longest['Dirs'] = len(folder)

                    if self.Info.Longest['File'] < len(file):
                        self.Info.Longest['File'] = len(file)

                    if self.Info.Longest['Size'] < len(self.GetSizeStr(size)):
                        self.Info.Longest['Size'] = len(self.GetSizeStr(size))


    # Text alignment
    def Left(self, text: str, width: int, fill: str = ' '):
        if len(text) > width:
            return text
        while len(text) < width:
            text += fill
        return text

    def Right(self, text: str, width: int, fill: str = ' '):
        if len(text) > width:
            return text
        while len(text) < width:
            text = fill + text
        return text

    def Center(self, text: str, width: str, fill: str = ' '):
        if len(text) > width:
            return text
        while len(text) < width:
            text = fill + text + fill
        if len(text) > width:
            text = text[1:]
        return text

        #def GetTSize(self):
        #    if self.TotalSize < 1000:
        #        return "{} B".format(self.TotalChars, 2)
        #    elif self.TotalSize < 10000000:
        #        return "{:.{}f} KB".format(self.TotalChars / 1000, 2)
        #    else:
        #        return "{:.{}f} GB".format(self.TotalChars / 10000000, 2)