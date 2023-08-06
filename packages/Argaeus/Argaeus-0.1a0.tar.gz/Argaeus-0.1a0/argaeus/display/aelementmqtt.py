from argaeus.display.aelement import AElement


class AElementMQTT(AElement):
    _mqtt_client = None
    _topic_sub = None

    def __init__(self, config, config_topics_sub, verbose, mqtt_client):
        AElement.__init__(self, config, verbose)
        self._mqtt_client = mqtt_client
        group, element = self._config["topic-sub"].split(".")
        self._topic_sub = config_topics_sub[group][element]
        self._mqtt_client.subscribe(self._topic_sub, self._topic_sub_handler)

    def _topic_sub_handler(self, value):
        raise NotImplementedError
