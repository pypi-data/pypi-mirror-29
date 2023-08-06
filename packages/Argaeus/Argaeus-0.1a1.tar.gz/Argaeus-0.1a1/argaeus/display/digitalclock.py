from argaeus.display.aelement import AElement
from PIL import ImageFont
from PIL import ImageDraw
import time
import os


class DigitalClock(AElement):
    _font = None
    _size = None
    _image_font = None

    def __init__(self, config, verbose):
        AElement.__init__(self, config, verbose)

        self._font = os.path.expanduser(self._config["font"])
        self._size = self._config["size"]
        self._image_font = ImageFont.truetype(self._font, self._size)

    def start(self):
        if self._verbose:
            print("DigitalClock.start()")
        pass

    def stop(self):
        if self._verbose:
            print("DigitalClock.stop()")
        pass

    def update_image(self):
        if self._verbose:
            print("DigitalClock.updateImage()")
        # clear image
        draw = ImageDraw.Draw(self.img)
        draw.rectangle((0, 0, self._width, self._height), fill=self._background_color)
        # write time
        t = time.strftime('%H:%M')
        w, h = draw.textsize(t, self._image_font)
        x = int((self._width - w) / 2)
        y = int((self._height - h) / 2)
        draw.text((x, y), t, font=self._image_font, fill=self._foreground_color)
