from argaeus.display.aelement import AElement
from PIL import ImageFont
from PIL import ImageDraw
import os


class SetPointText:
    _font = None
    _size = None
    _string = None
    _state = None

    def __init__(self, config, verbose, state):
        AElement.__init__(self, config, verbose)
        self._state = state

        self._font = os.path.expanduser(self._config["font"])
        self._size = self._config["size"]
        self._image_font = ImageFont.truetype(self._font, self._size)
        self._string = config["string"]

    def start(self):
        if self._verbose:
            print("SetPointText.start()")
        pass

    def stop(self):
        if self._verbose:
            print("SetPointText.stop()")
        pass

    def update_image(self):
        if self._verbose:
            print("SetPointText.updateImage()")
        # clear image
        draw = ImageDraw.Draw(self.img)
        draw.rectangle((0, 0, self._width, self._height), fill=self._background_color)
        # write time
        text = ""
        value = self._state.current_program.set_point
        if value is not None:
            text = self._string.format(value)
        if self._verbose:
            print("SetPointText.updateImage() - string '{}', value '{}', text '{}'".
                  format(self._string, value, text))
        w, h = draw.textsize(text, self._image_font)
        x = int((self._width - w) / 2)
        y = int((self._height - h) / 2)
        draw.text((x, y), text, font=self._image_font, fill=self._foreground_color)

