from argaeus.controller.acontroller import AController
from argaeus.controller.behavior.behaviorworker import BehaviorWorker
from argaeus.controller.behavior.buttonbehavior import ButtonBehavior


class OperationController(AController):
    _mqtt_client = None
    _state = None

    _default_is_active = None
    
    _topic_pub = None
    _command_active = None
    _command_passive = None

    def __init__(self, config, verbose, state, mqtt_client, config_topics_pub, config_mqtt_translations):
        AController.__init__(self, config, verbose, None, config_topics_pub, config_mqtt_translations)
        self._mqtt_client = mqtt_client
        self._state = state

        self._default_is_active = bool(self._config["default-is-active"])
        self._state.active_operation = self._default_is_active

        self._topic_pub = self._get_topic_pub(self._config["topic-pub"])
        self._command_active = self._get_mqtt_translations(self._config["command-active"])
        self._command_passive = self._get_mqtt_translations(self._config["command-passive"])

        self._behavior_worker = BehaviorWorker(self._verbose, self._state, ButtonBehavior.ToggleActivePassive,
                                               self._worker_executor)

    def _worker_executor(self, item):
        self._state.active_operation = not self._state.active_operation
        if self._verbose:
            print("OperationController._worker_executor - toggle active/passive (now: '{}').".
                  format(self._state.active_operation))
        self._publish()

    def _publish(self):
        if self._state.active_operation:
            self._mqtt_client.publish(self._topic_pub, self._command_active)
        else:
            self._mqtt_client.publish(self._topic_pub, self._command_passive)

    def start(self):
        self._publish()
        self._behavior_worker.start()

    def stop(self):
        self._behavior_worker.stop()
