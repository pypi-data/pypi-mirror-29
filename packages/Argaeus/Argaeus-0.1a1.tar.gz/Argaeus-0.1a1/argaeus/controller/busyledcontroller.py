from argaeus.controller.acontroller import AController


class BusyLedController(AController):
    _mqtt_client = None

    _topic_pub = None
    _topic_sub = None
    _command_on = None
    _command_off = None

    def __init__(self, config, verbose, mqtt_client, config_topics_sub, config_topics_pub, config_mqtt_translations):
        AController.__init__(self, config, verbose, config_topics_sub, config_topics_pub, config_mqtt_translations)
        self._mqtt_client = mqtt_client

        self._topic_sub = self._get_topic_sub(self._config["topic-sub"])
        self._topic_pub = self._get_topic_pub(self._config["topic-pub"])
        self._command_on = self._get_mqtt_translations(self._config["command-on"])
        self._command_off = self._get_mqtt_translations(self._config["command-off"])

    def _topic_sub_handler(self, value):
        value = int(value)
        if value == 0:
            self._mqtt_client.publish(self._topic_pub, self._command_off)
        elif value > 0:
            self._mqtt_client.publish(self._topic_pub, self._command_on)
        else:
            raise ValueError("BusyLedController._topic_sub_handler - dont know what to do with value '{}'.".format(value))

    def start(self):
        self._mqtt_client.publish(self._topic_pub, self._command_off)
        self._mqtt_client.subscribe(self._topic_sub, self._topic_sub_handler)

    def stop(self):
        self._mqtt_client.unsubscribe(self._topic_sub, self._topic_sub_handler)
