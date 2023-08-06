from argaeus.controller.behavior.buttonbehavior import ButtonBehavior


class Behavior:
    _config = None
    _verbose = None
    _mqtt_client = None
    _state = None

    _name = None
    _topic_sub = None
    _topic_command = None
    _behavior = None

    def __init__(self, config, verbose, state, mqtt_client, config_topics_sub, config_mqtt_translations):
        self._verbose = verbose
        self._config = config
        self._mqtt_client = mqtt_client
        self._state = state
        if self._verbose:
            print("Behavior.__init__ - initializing instance ('{}').".format(self._config))

        self._name = self._config["name"]

        group, element = self._config["topic-sub"].split(".")
        self._topic_sub = config_topics_sub[group][element]
        group, element = self._config["mqtt-translation"].split(".")
        self._topic_command = config_mqtt_translations[group][element]

        self._behavior = ButtonBehavior.factory(self._config["behavior"])

    def _topic_handler(self, value):
        if value.decode("utf-8")  == self._topic_command:
            if self._verbose:
                print("Behavior._topic_handler - detected behavior '{}' from input '{}'.".
                      format(self._behavior._name_, self._name))
            self._state.behavior_queues[self._behavior].put(True)
        else:
            if self._verbose:
                print("Behavior._topic_handler - received unknown value '{}'".format(value))

    def start(self):
        if self._verbose:
            print("Behavior.start - subscribing topic.")
        self._mqtt_client.subscribe(self._topic_sub, self._topic_handler)

    def stop(self):
        if self._verbose:
            print("Behavior.start - unsubscribing topic.")
        self._mqtt_client.unsubscribe(self._topic_sub, self._topic_handler)
