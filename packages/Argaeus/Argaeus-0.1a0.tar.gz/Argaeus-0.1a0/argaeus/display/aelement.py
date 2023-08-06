from PIL import Image


class AElement:
    _config = None
    _verbose = None
    name = None
    img = None
    _width = None
    _height = None
    x = None
    y = None
    _foreground_color = None
    _background_color = None

    def __init__(self, config, verbose):
        self._config = config
        self._verbose = verbose
        if verbose:
            print("{}.__init__ - creating instance ('{}').".format(self.__class__.__name__, config))
        if not self.__class__.__name__.lower() == self._config["type"].lower():
            raise ValueError("type '{}' as given in config is not equvivalent to class type '{}'.".
                             format(self._config["type"].lower(), self.__class__.__name__.lower()))
        self.name = self._config["name"]

        self._width = int(self._config["width"])
        self._height = int(self._config["height"])
        self.x = int(self._config["x"])
        self.y = int(self._config["y"])
        self._foreground_color = int(self._config["foreground-color"])
        self._background_color = int(self._config["background-color"])

        if self._foreground_color not in [0,255]:
            raise ValueError("AElement.'{}' - foreground-color must be 0 or 255 ('{}').".
                             format(self.name, self._foreground_color))
        if self._background_color not in [0,255]:
            raise ValueError("AElement.'{}' - background-color must be 0 or 255 ('{}').".
                             format(self.name, self._background_color))

        self.img = Image.new('1', (self._width, self._height), self._background_color)

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def update_image(self):
        raise NotImplementedError
