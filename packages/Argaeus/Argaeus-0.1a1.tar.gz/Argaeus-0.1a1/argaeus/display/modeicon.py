from argaeus.display.aelement import AElement
from PIL import Image
import os


class ModeIcon(AElement):
    _get_current_mode_fct = None
    _state = None

    def __init__(self, config, verbose, state):
        AElement.__init__(self, config, verbose)
        self._state = state

    def start(self):
        if self._verbose:
            print("ModeIcon.start()")
        pass

    def stop(self):
        if self._verbose:
            print("ModeIcon.stop()")
        pass

    def update_image(self):
        icon = self._state.current_mode.icon
        w,h = icon.size
        x = int((self._width - w) / 2)
        y = int((self._height - h) / 2)
        self.img = Image.new('1', (self._width, self._height), self._background_color)
        self.img.paste(icon, (x, y))
