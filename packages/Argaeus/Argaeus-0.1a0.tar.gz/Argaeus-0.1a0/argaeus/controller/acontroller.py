class AController:
    _config = None
    _verbose = None
    _config_topics_sub = None
    _config_topics_pub = None
    _config_mqtt_translations = None

    def __init__(self, config, verbose, config_topics_sub, config_topics_pub, config_mqtt_translations):
        self._config = config
        self._verbose = verbose
        if self._verbose:
            print("{}.__init__ - initializing instance(''{}').".format(self.__class__.__name__, self._config))

        self._config_topics_sub = config_topics_sub
        self._config_topics_pub = config_topics_pub
        self._config_mqtt_translations = config_mqtt_translations

    def _get_topic_sub(self, name):
        group, entry = name.split(".")
        return self._config_topics_sub[group][entry]

    def _get_topic_pub(self, name):
        group, entry = name.split(".")
        return self._config_topics_pub[group][entry]

    def _get_mqtt_translations(self, name):
        group, entry = name.split(".")
        return self._config_mqtt_translations[group][entry]

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
