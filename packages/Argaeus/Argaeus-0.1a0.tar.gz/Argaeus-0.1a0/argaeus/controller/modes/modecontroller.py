import datetime
from argaeus.controller.modes.modefactory import ModeFactory
from argaeus.controller.modes.modeschedule import ModeSchedule
from argaeus.controller.acontroller import AController
from argaeus.controller.behavior.buttonbehavior import ButtonBehavior
from argaeus.controller.behavior.behaviorworker import BehaviorWorker


class ModeController(AController):
    _state = None
    _mqtt_client = None

    _modes = None
    _selectable_modes = None
    _selectable_pos = None
    _default_mode = None

    _topic_sub_left = None
    _command_left = None
    _topic_sub_right = None
    _command_right = None

    def __init__(self, config, verbose, state, mqtt_client, config_modes, config_topics_sub, config_topics_pub,
                 config_mqtt_translations):
        AController.__init__(self, config, verbose, config_topics_sub, config_topics_pub, config_mqtt_translations)
        self._state = state
        self._mqtt_client = mqtt_client

        self._modes, self._selectable_modes = ModeFactory.create_modes(config_modes, self._verbose, mqtt_client,
                                                                       config_topics_pub)
        self._default_mode = self._modes[self._config["default-mode"]]
        self._activate_default_mode()

        self._topic_sub_left = self._get_topic_sub(self._config["topic-sub-left"])
        self._command_left = self._get_mqtt_translations(self._config["command-left"])
        self._topic_sub_right = self._get_topic_sub(self._config["topic-sub-right"])
        self._command_right = self._get_mqtt_translations(self._config["command-right"])

        self._behavior_worker = BehaviorWorker(self._verbose, self._state, ButtonBehavior.ToDefaultMode,
                                               self._worker_executor)

    def _activate_default_mode(self):
        self._selectable_pos = self._selectable_modes.index(self._default_mode)
        self._state.current_mode = self._default_mode
        if isinstance(self._state.current_mode, ModeSchedule):
            dt = datetime.datetime.time(datetime.datetime.now())
            self._state.current_program = self._state.current_mode.get_program_at_time(dt)
        else:
            self._state.current_program = self._state.current_mode

    def _worker_executor(self, item):
        if self._verbose:
            print("ModeController._worker_executor - activate default mode")
        self._activate_default_mode()
        self.update()

    def _topic_handler_left(self, value):
        if value.decode("utf-8") == self._command_left:
            if self._verbose:
                print("ModeController._topic_handler - command left.")
            self._selectable_pos = self._selectable_pos - 1
            self._post_topic_handler()

    def _topic_handler_right(self, value):
        if value.decode("utf-8") == self._command_right:
            if self._verbose:
                print("ModeController._topic_handler - command right.")
            self._selectable_pos = self._selectable_pos + 1
            self._post_topic_handler()

    def _post_topic_handler(self):
        self._selectable_pos = self._selectable_pos % len(self._selectable_modes)
        self._state.current_mode = self._selectable_modes[self._selectable_pos]
        if self._verbose:
            print("ModeController._topic_handler - selected mode '{}' at pos '{}'.".
                  format(self._state.current_mode.name, self._selectable_pos))
        self.update()

    def update(self):
        if isinstance(self._state.current_mode, ModeSchedule):
            dt = datetime.datetime.time(datetime.datetime.now())
            self._state.current_program = self._state.current_mode.get_program_at_time(dt)
            self._state.current_schedule = self._state.current_mode.schedule_raw
        else:
            self._state.current_program = self._state.current_mode
            self._state.current_schedule = None
        self._state.current_program.publish()
        self._state.update_display.set()

    def start(self):
        self._mqtt_client.subscribe(self._topic_sub_left, self._topic_handler_left)
        self._mqtt_client.subscribe(self._topic_sub_right, self._topic_handler_right)
        self._state.current_program.publish()
        self._behavior_worker.start()
        self.update()

    def stop(self):
        self._mqtt_client.unsubscribe(self._topic_sub_left, self._topic_handler_left)
        self._mqtt_client.unsubscribe(self._topic_sub_right, self._topic_handler_right)
        self._behavior_worker.stop()
