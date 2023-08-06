from argaeus.controller.acontroller import AController
from argaeus.controller.behavior.buttonbehavior import ButtonBehavior
from argaeus.controller.behavior.behaviorworker import BehaviorWorker


class SetPointController(AController):
    _state = None
    _mqtt_client = None

    _step_size = None
    _min_temp = None
    _max_temp = None

    _topic_sub_left = None
    _command_left = None
    _topic_sub_right = None
    _command_right = None

    _behavior_worker = None

    def __init__(self, config, verbose, state, mqtt_client, config_topics_sub, config_mqtt_translations):
        AController.__init__(self, config, verbose, config_topics_sub, None, config_mqtt_translations)
        self._state = state
        self._mqtt_client = mqtt_client

        self._step_size = float(self._config["step-size"])
        self._min_temp = float(self._config["min-temp"])
        self._max_temp = float(self._config["max-temp"])

        self._topic_sub_left = self._get_topic_sub(self._config["topic-sub-left"])
        self._command_left = self._get_mqtt_translations(self._config["command-left"])
        self._topic_sub_right = self._get_topic_sub(self._config["topic-sub-right"])
        self._command_right = self._get_mqtt_translations(self._config["command-right"])

        self._behavior_worker = BehaviorWorker(self._verbose, self._state, ButtonBehavior.ResetToDefaultTemp,
                                               self._worker_executor)

    def _worker_executor(self, item):
        if self._verbose:
            print("SetPointController._worker_executor - reset to default set point.")
        self._post_topic_handler(self._state.current_program.default_set_point)

    def _topic_handler_left(self, value):
        if value.decode("utf-8")  == self._command_left:
            if self._verbose:
                print("SetPointController._topic_handler - command left.")
            set_point = self._state.current_program.set_point - self._step_size
            self._post_topic_handler(set_point)

    def _topic_handler_right(self, value):
        if value.decode("utf-8")  == self._command_right:
            if self._verbose:
                print("SetPointController._topic_handler - command right.")
            set_point = self._state.current_program.set_point + self._step_size
            self._post_topic_handler(set_point)

    def _post_topic_handler(self, set_to):

        set_point = min(self._max_temp, max(self._min_temp, set_to))
        if self._verbose:
            print("SetPointController._topic_handler - set temp to '{}'.".format(self._state.current_mode.name))
        self._state.current_program.set_point = set_point
        self._state.current_program.publish()
        self._state.update_display.set()

    def start(self):
        self._mqtt_client.subscribe(self._topic_sub_left, self._topic_handler_left)
        self._mqtt_client.subscribe(self._topic_sub_right, self._topic_handler_right)
        self._behavior_worker.start()

    def stop(self):
        self._mqtt_client.unsubscribe(self._topic_sub_left, self._topic_handler_left)
        self._mqtt_client.unsubscribe(self._topic_sub_right, self._topic_handler_right)
        self._behavior_worker.stop()
