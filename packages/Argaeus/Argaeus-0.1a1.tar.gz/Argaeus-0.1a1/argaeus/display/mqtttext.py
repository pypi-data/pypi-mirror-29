from argaeus.display.aelementmqtt import AElementMQTT
from PIL import ImageFont
from PIL import ImageDraw
import os


class MQTTText(AElementMQTT):
    _font = None
    _size = None
    _string = None
    _current_value = None

    def __init__(self, config, config_topics_sub, verbose, mqtt_client):
        AElementMQTT.__init__(self, config, config_topics_sub, verbose, mqtt_client)

        self._font = os.path.expanduser(self._config["font"])
        self._size = self._config["size"]
        self._image_font = ImageFont.truetype(self._font, self._size)
        self._string = config["string"]

    def _topic_sub_handler(self, value):
        if self._verbose:
            print("MQTTText._topic_sub_handler - received value '{}'.".format(value))
        self._current_value = float(value)

    def start(self):
        if self._verbose:
            print("MQTTText.start()")
        pass

    def stop(self):
        if self._verbose:
            print("MQTTText.stop()")
        pass

    def update_image(self):
        if self._verbose:
            print("MQTTText.updateImage()")
        # clear image
        draw = ImageDraw.Draw(self.img)
        draw.rectangle((0, 0, self._width, self._height), fill=self._background_color)
        # write time
        text = ""
        if self._current_value is not None:
            text = self._string.format(self._current_value)
        if self._verbose:
            print("MQTTText.updateImage() - string '{}', value '{}', text '{}'".
                  format(self._string, self._current_value, text))
        w, h = draw.textsize(text, self._image_font)
        x = int((self._width - w) / 2)
        y = int((self._height - h) / 2)
        draw.text((x, y), text, font=self._image_font, fill=self._foreground_color)

