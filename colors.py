class Colors:
    __instance = None

    @staticmethod
    def Get():
        if Colors.__instance is None:
            Colors()
        return Colors.__instance

    def __init__(self):
        if Colors.__instance is not None:
            return
        else:
            Colors.__instance = self
            self.DarkMode()
            self.themes = dict(
                DARK = lambda: self.DarkMode(),
                LIGHT = lambda: self.LightMode()
            )

    def Set(self, theme: str) -> bool:
        theme = theme.upper()
        for key, value in self.themes.items():
            if theme == key:
                value()
                return True
        return False


    def LightMode(self):
        self.FRAME_BG1 = "#FFFFFF"
        self.FRAME_BG2 = "#EFEFEF"

        self.TEXT_FG = "#000000"
        self.LABEL_FG = "#000000"
        self.BUTTON_FG = "#000000"

    def DarkMode(self):
        self.FRAME_BG1 = "#4C4E52"
        self.FRAME_BG2 = "#3b3d41"

        self.TEXT_FG = "#FFFFFF"
        self.LABEL_FG = "#FFFFFF"
        self.BUTTON_FG = "#FFFFFF"