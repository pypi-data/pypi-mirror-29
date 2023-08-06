from argaeus.controller.modes.amode import AMode


class ModeProgram(AMode):
    set_point = None
    default_set_point = None
    _mqtt_client = None
    _topic_pub = None

    def __init__(self, config, verbose, mqtt_client, config_topics_pub):
        AMode.__init__(self, config, verbose)
        self.set_point = float(self._config["set-point"])
        self.default_set_point = self.set_point
        self._mqtt_client = mqtt_client
        self._topic_pub = config_topics_pub["temperature"]["set-point"]

    def publish(self):
        self._mqtt_client.publish(self._topic_pub, self.set_point)

