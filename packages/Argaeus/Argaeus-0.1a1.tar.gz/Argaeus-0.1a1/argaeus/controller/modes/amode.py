from PIL import Image
import os


class AMode:
    _config = None
    _verbose = None

    name = None
    selectable = None
    icon = None

    def __init__(self, config, verbose):
        self._config = config
        self._verbose = verbose
        self.name = self._config["name"]
        if self._verbose:
            print("{}.__init__ - initializing {} ('{}').".format(self.__class__.__name__, self.name, self._config))

        self.selectable = bool(self._config["selectable"])
        icon_path = os.path.expanduser(self._config["icon"])
        self.icon = Image.open(icon_path)
