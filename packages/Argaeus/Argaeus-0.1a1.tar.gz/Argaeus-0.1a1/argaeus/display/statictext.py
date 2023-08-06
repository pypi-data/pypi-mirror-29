from argaeus.display.aelement import AElement
from PIL import ImageFont
from PIL import ImageDraw
import os


class StaticText:
    _font = None
    _size = None
    _string = None

    def __init__(self, config, verbose):
        AElement.__init__(self, config, verbose)

        self._font = os.path.expanduser(self._config["font"])
        self._size = self._config["size"]
        self._image_font = ImageFont.truetype(self._font, self._size)
        self._string = config["string"]

    def start(self):
        if self._verbose:
            print("StaticText.start()")
        pass

    def stop(self):
        if self._verbose:
            print("StaticText.stop()")
        pass

    def update_image(self):
        if self._verbose:
            print("StaticText.updateImage()")
        # clear image
        draw = ImageDraw.Draw(self.img)
        draw.rectangle((0, 0, self._width, self._height), fill=self._background_color)
        # write time
        if self._verbose:
            print("SetPointText.updateImage() - string '{}'.".format(self._string))
        w, h = draw.textsize(self._string, self._image_font)
        x = int((self._width - w) / 2)
        y = int((self._height - h) / 2)
        draw.text((x, y), self._string, font=self._image_font, fill=self._foreground_color)

