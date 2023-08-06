import math
from argaeus.display.aelementmqtt import AElementMQTT
from PIL import Image


class Bar(AElementMQTT):
    _current_value = None
    _min_value = None
    _max_value = None
    _normalize_to = None

    def __init__(self, config, config_topics_sub, verbose, mqtt_client):
        AElementMQTT.__init__(self, config, config_topics_sub, verbose, mqtt_client)

        self._max_value = float(self._config["max-value"])
        self._min_value = float(self._config["min-value"])
        self._normalize_to = math.log(self._max_value - self._min_value + 1)

        self._current_value = min(self._max_value, max(self._min_value, float(0)))

    def _topic_sub_handler(self, value):
        self._current_value = min(self._max_value, max(self._min_value, float(value)))
        if self._verbose:
            print("Bar._topic_sub_handler - received value '{}' -> current value '{}'.".
                  format(value, self._current_value))

    def start(self):
        if self._verbose:
            print("Bar.start()")
        pass

    def stop(self):
        if self._verbose:
            print("Bar.stop()")
        pass

    def _get_bar_height(self):
        value = self._current_value - self._min_value + 1
        if self._verbose:
            print("Bar._get_bar_height - value: {}, internal value: {}, min: {}, height: {}.".
                  format(self._current_value, value, self._min_value, self._height))
        norm_value = math.log(value) / self._normalize_to
        bar_height = int((self._height - 1) * norm_value) + 1  # +/- 1 sets height of bar to 1 for value 0.
        return bar_height

    def update_image(self):
        bar_height = self._get_bar_height()
        if self._verbose:
            print("Bar.updateImage() - volt '{}', bar height '{}'".
                  format(self._current_value, bar_height))
        # create image
        self.img = Image.new("1", (self._width, bar_height), self._foreground_color)


