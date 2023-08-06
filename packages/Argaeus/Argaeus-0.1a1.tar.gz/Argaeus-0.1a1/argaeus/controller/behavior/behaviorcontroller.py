from argaeus.controller.acontroller import AController
from argaeus.controller.behavior.behavior import Behavior


class BehaviorController:
    _behaviors = None

    def __init__(self, config, verbose, state, mqtt_client, config_topics_sub, config_mqtt_translations):
        AController.__init__(self, config, verbose, config_topics_sub, None, config_mqtt_translations)

        self._behaviors = []
        for c in config:
            b = Behavior(c, verbose, state, mqtt_client, config_topics_sub, config_mqtt_translations)
            self._behaviors.append(b)

    def start(self):
        for b in self._behaviors:
            b.start()

    def stop(self):
        for b in self._behaviors:
            b.stop()
