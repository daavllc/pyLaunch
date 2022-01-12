class Style:
    __instance = None

    @staticmethod
    def Get():
        if Style.__instance is None:
            Style()
        return Style.__instance

    def __init__(self):
        if Style.__instance is not None:
            return
        else:
            Style.__instance = self
            self.ThemeDark()
            self.themes = dict(
                DARK = lambda: self.ThemeDark(),
                LIGHT = lambda: self.ThemeLight(),
                MIDNIGHT = lambda: self.ThemeMidnight(),
                DARK_BLUE = lambda: self.ThemeDarkBlue(),
                LIGHT_BLUE = lambda: self.ThemeLightBlue(),
                AMARANTH = lambda: self.ThemeAmaranth()
            )
            self.FONT = "Arial"

            self.SIZE_TITLE = 16
            self.SIZE_TEXT = 10
            self.SIZE_TEXT_SMALL = 8
            self.SIZE_TEXT_LARGE = 12

            self.FONT_TITLE = (self.FONT, self.SIZE_TITLE)
            self.FONT_TEXT = (self.FONT, self.SIZE_TEXT)
            self.FONT_TEXT_SMALL = (self.FONT, self.SIZE_TEXT_SMALL)
            self.FONT_TEXT_LARGE = (self.FONT, self.SIZE_TEXT_LARGE)
            self.FONT_TEXT_MONO = ("TkFixedFont", self.SIZE_TEXT)


            self.PAD_TEXTX = 5
            self.PAD_TEXTY = 5

            self.PAD_BUTTONX = 5
            self.PAD_BUTTONY = 5

            self.PAD_HEADERX = 5

            self.PAD_BODY = 15


    def Set(self, theme: str) -> bool:
        theme = theme.upper()
        for key, value in self.themes.items():
            if theme == key:
                value()
                return True
        return False

    def GetThemes(self) -> list:
        themes = []
        for key in self.themes.keys():
            themes.append(key.lower())
        return themes

    def ThemeLight(self):
        self.FRAME_BG = "#EFEFEF"
        self.FRAME_BG_ALT = "#FFFFFF"

        self.TEXT_FG    = "#000000"
        self.TEXT_BG    = self.FRAME_BG
        self.TEXT_ERROR = "#2200000"

        self.LABEL_FG   = "#000000"
        self.LABEL_BG   = self.FRAME_BG

        self.BUTTON_FG  = "#000000"
        self.BUTTON_BG  = self.FRAME_BG
        self.BUTTON_HOVER = self._ChangeColor(20, self.BUTTON_BG)
        self.BUTTON_PRESS = self._ChangeColor(-20, self.BUTTON_BG)

    def ThemeDark(self):
        self.FRAME_BG = "#3b3d41"
        self.FRAME_BG_ALT = "#4C4E52"

        self.TEXT_FG    = "#FFFFFF"
        self.TEXT_BG    = self.FRAME_BG
        self.TEXT_ERROR = "#FF0000"

        self.LABEL_FG   = "#FFFFFF"
        self.LABEL_BG   = self.FRAME_BG

        self.BUTTON_FG  = "#FFFFFF"
        self.BUTTON_BG  = self.FRAME_BG
        self.BUTTON_HOVER = self._ChangeColor(20, self.BUTTON_BG)
        self.BUTTON_PRESS = self._ChangeColor(-20, self.BUTTON_BG)

    def ThemeMidnight(self):
        self.FRAME_BG = "#111111"
        self.FRAME_BG_ALT = "#1F1F1F"

        self.TEXT_FG    = "#FFFFFF"
        self.TEXT_BG    = self.FRAME_BG
        self.TEXT_ERROR = "#FF00000"

        self.LABEL_FG   = "#FFFFFF"
        self.LABEL_BG   = self.FRAME_BG

        self.BUTTON_FG  = "#FFFFFF"
        self.BUTTON_BG  = self.FRAME_BG
        self.BUTTON_HOVER = self._ChangeColor(20, self.BUTTON_BG)
        self.BUTTON_PRESS = self._ChangeColor(-20, self.BUTTON_BG)

    def ThemeDarkBlue(self):
        self.FRAME_BG = "#000055"
        self.FRAME_BG_ALT = "#000066"

        self.TEXT_FG    = "#FFFFFF"
        self.TEXT_BG    = self.FRAME_BG
        self.TEXT_ERROR = "#FF0000"

        self.LABEL_FG   = "#FFFFFF"
        self.LABEL_BG   = self.FRAME_BG

        self.BUTTON_FG  = "#FFFFFF"
        self.BUTTON_BG  = self.FRAME_BG
        self.BUTTON_HOVER = self._ChangeColor(20, self.BUTTON_BG)
        self.BUTTON_PRESS = self._ChangeColor(-20, self.BUTTON_BG)

    def ThemeLightBlue(self):
        self.FRAME_BG = "#5DB3CE"
        self.FRAME_BG_ALT = "#86C5DA"

        self.TEXT_FG    = "#000000"
        self.TEXT_BG    = self.FRAME_BG
        self.TEXT_ERROR = "#880000"

        self.LABEL_FG   = "#000000"
        self.LABEL_BG   = self.FRAME_BG

        self.BUTTON_FG  = "#000000"
        self.BUTTON_BG  = self.FRAME_BG
        self.BUTTON_HOVER = self._ChangeColor(20, self.BUTTON_BG)
        self.BUTTON_PRESS = self._ChangeColor(-20, self.BUTTON_BG)

    def ThemeAmaranth(self):
        self.FRAME_BG = "#E1414C"
        self.FRAME_BG_ALT = "#E86D76"

        self.TEXT_FG    = "#000000"
        self.TEXT_BG    = self.FRAME_BG
        self.TEXT_ERROR = "#000088"

        self.LABEL_FG   = "#000000"
        self.LABEL_BG   = self.FRAME_BG

        self.BUTTON_FG  = "#000000"
        self.BUTTON_BG  = self.FRAME_BG
        self.BUTTON_HOVER = self._ChangeColor(20, self.BUTTON_BG)
        self.BUTTON_PRESS = self._ChangeColor(-20, self.BUTTON_BG)

    def _ChangeColor(self, value: int, color: str) -> str:
        newColor = "#"
        color = color[1:]

        # convert each section to it's RGB value [0-255]
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        for section in [r, g, b]:
            newSection = int(hex(int(str(section + value), 16)).replace("0x", ""))
            if newSection > 255:
                newColor += "FF"
            elif newSection < 0:
                newColor += "00"
            else:
                newColor += hex(newSection).replace("0x", "").zfill(2)
        return newColor
