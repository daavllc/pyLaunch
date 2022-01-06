
from .cui import CUI
from .gui import GUI
from .serializer import Deserialize
from .configuration import Configuration

class Configurator:
    def __init__(self):
        self.Configuration = Configuration()

    def New(self, UI: str) -> bool:
        """ Launcher has not been configured, so let's configure it """
        if UI == "GUI":
            self.UI = GUI()
        else:
            self.UI = CUI()
        return self.UI.Launch() # This uses the specified UI, creates the configuration, and serializes it
        

    def Load(self) -> None:
        """ Launcher is configured, load that configuration and execute """
        self.Configuration.data = Deserialize()
