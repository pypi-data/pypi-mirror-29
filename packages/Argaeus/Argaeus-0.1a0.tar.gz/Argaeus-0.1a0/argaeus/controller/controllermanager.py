from argaeus.controller.behavior.behaviorcontroller import BehaviorController
from argaeus.controller.busyledcontroller import BusyLedController
from argaeus.controller.modes.modecontroller import ModeController
from argaeus.controller.setpointcontroller import SetPointController
from argaeus.controller.operationcontroller import OperationController


class ControllerManager:
    _config = None
    _verbose = None

    _mode_controller = None
    _behavior_controller = None
    _busyled_controller = None
    _set_point_controller = None
    _operation_controller = None

    def __init__(self, config, verbose, state, mqtt_client):
        self._config = config
        self._verbose = verbose
        if self._verbose:
            print("ControllerManager.__init__ - initializing ControllerManager ('{}').".format(self._config))

        self._busyled_controller = BusyLedController(config["controller"]["busy-led-controller"], verbose, mqtt_client,
                                                     self._config["topics-sub"], self._config["topics-pub"],
                                                     self._config["mqtt-translations"])
        self._behavior_controller = BehaviorController(self._config["controller"]["button-controller"], self._verbose,
                                                       state, mqtt_client, self._config["topics-sub"],
                                                       self._config["mqtt-translations"])
        self._mode_controller = ModeController(self._config["controller"]["mode-controller"], self._verbose, state,
                                               mqtt_client, self._config["modes"], self._config["topics-sub"],
                                               self._config["topics-pub"], self._config["mqtt-translations"])
        self._set_point_controller = SetPointController(self._config["controller"]["setpoint-controller"],
                                                        self._verbose, state, mqtt_client, self._config["topics-sub"],
                                                        self._config["mqtt-translations"])
        self._operation_controller = OperationController(self._config["controller"]["operation-controller"],
                                                        self._verbose, state, mqtt_client, self._config["topics-pub"],
                                                        self._config["mqtt-translations"])
        if self._verbose:
            print("ControllerManager.__init__ - done.")

    def update(self):
        self._mode_controller.update()

    def start(self):
        self._busyled_controller.start()
        self._behavior_controller.start()
        self._mode_controller.start()
        self._set_point_controller.start()
        self._operation_controller.start()

    def stop(self):
        self._busyled_controller.stop()
        self._behavior_controller.stop()
        self._mode_controller.stop()
        self._set_point_controller.stop()
        self._operation_controller.stop()
