from PIL import Image
import threading
import time
import os
from argaeus.tools.epapermqttmessageconverter import EPaperMQTTMessageEncoder


class Display:
    _config = None
    _verbose = None
    _elements = None

    _width = None
    _height = None

    _lock_update = None

    _mqtt_client = None

    last_image = None
    _base_image = None
    _background_image = None

    _state = None
    _handle_for_update_display_events = None
    _stop_loop = None

    _wipe_screen_at_startup = None

    def __init__(self, config, verbose, state, elements, mqtt_client, topics_pub):
        self._verbose = verbose
        self._config = config
        self._state = state
        if self._verbose:
            print("Display.__init__ - creating instance ('{}', '{}').".format(config, topics_pub))
        self._elements = elements
        self._lock_update = threading.Lock()
        self._mqtt_client = mqtt_client

        self._topic_full_image = topics_pub["epaper"]["full_image"]
        self._topic_full_image_twice = topics_pub["epaper"]["full_image_twice"]
        self._topic_partial_image = topics_pub["epaper"]["part_image"]
        self._topic_partial_image_twice = topics_pub["epaper"]["part_image_twice"]

        self._width = int(self._config["width"])
        self._height = int(self._config["height"])
        self._background_color = int(self._config["background-color"])
        if self._background_color not in [0,255]:
            raise ValueError("Display.__init__ - background-color must be 0 or 255 ('{}').".
                             format(self._background_color))

        self._background_image = Image.open(os.path.expanduser(self._config["background"]))
        self._base_image = Image.new('1', (self._width, self._height), self._background_color)
        self._base_image.paste(self._background_image, (0,0))
        self.last_image = self._base_image.copy()

        self._wipe_screen_at_startup = bool(self._config["wipe-screen"]["at-startup"])
        self._handle_for_update_display_events = threading.Thread(target=self._update_display_thread)
        self._stop_loop = threading.Event()
        self._stop_loop.clear()

        if self._verbose:
            print("Display.__init__ - done.")

    def _update_display_thread(self):
        while not self._stop_loop.isSet():
            if self._state.update_display.wait(0.5):
                self.update()

    def update(self):
        if self._verbose:
            print("Display.update - update display ... waiting for lock")
        with self._lock_update:
            self._state.update_display.clear()  # maybe not necessary to be called - racingcondition between
                                                 # time event and update display event could occoure ...
            self._update_elements()
            new_image = self._merge_elements_to_new_image()
            self._update_display(new_image)
        if self._verbose:
            print("Display.update - update display ... released lock")

    def _update_elements(self):
        if self._verbose:
            print("Display._update_elements - update display")
        for element in self._elements:
            try:
                element.update_image()
            except NotImplementedError:
                pass

    def _merge_elements_to_new_image(self):
        if self._verbose:
            print("Display._merge_elements - create new image with the display")
        new_image = self._base_image.copy()
        for element in self._elements:
            new_image.paste(element.img, (element.x, element.y))
        return new_image

    def _update_display(self, new_image):
        message = EPaperMQTTMessageEncoder.to_full_image_message(new_image)
        self._mqtt_client.publish(self._topic_full_image, message)
        self.last_image = new_image

    def _wipe_screen(self):
        if self._verbose:
            print("Display._wipe_screen - begin")
        with self._lock_update:
            img_white = Image.new('1', (self._width, self._height), 255)
            img_black = Image.new('1', (self._width, self._height), 255)
            msg_white = EPaperMQTTMessageEncoder.to_full_image_message(img_white)
            msg_black = EPaperMQTTMessageEncoder.to_full_image_message(img_black)
            for x in range(4):
                if self._verbose:
                    print("Display._wipe_screen - sending black&white combination (cycle {}).".format(x))
                self._mqtt_client.publish(self._topic_full_image_twice, msg_black)
                time.sleep(5)
                self._mqtt_client.publish(self._topic_full_image_twice, msg_white)
                time.sleep(5)
        if self._verbose:
            print("Display._wipe_screen - end")

    def start(self, skip_wipe_screen=False):  # skip_wipe_screen for testing purposes
        if self._verbose:
            print("Display.start")
        if self._wipe_screen_at_startup and not skip_wipe_screen:
            self._wipe_screen()
        if self._verbose:
            print("Display.start - starting {} elements.".format(len(self._elements)))
        for e in self._elements:
            try:
                e.start()
            except NotImplementedError:
                pass
        self._stop_loop.clear()
        self._handle_for_update_display_events.start()

    def stop(self):
        if self._verbose:
            print("Display.stop - stopping {} elements.".format(len(self._elements)))
        for e in self._elements:
            try:
                e.stop()
            except NotImplementedError:
                pass
        self._stop_loop.set()
        self._handle_for_update_display_events.join()
