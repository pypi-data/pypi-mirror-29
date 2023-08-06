import argparse
import os
import time
from pathlib import Path
from argaeus.display.display import Display
from argaeus.controller.controllermanager import ControllerManager
from argaeus.display.elementfactory import ElementFactory
from argaeus.state import State
from argaeus.tools import mypyyaml
from argaeus.tools.mqttclient import MQTTClient
from argaeus.tools.myinfluxdbclient import MyInfluxDBClient
import argaeus
import threading


class GUI:
    _config = None
    _verbose = None

    _mqtt_client = None
    _influxdb_client = None

    _state = None
    _display = None
    _controller = None

    _stop_loop = None
    _loop_thread = None
    _is_stopped = None

    def __init__(self, config, verbose):
        self._verbose = verbose
        self._config = config
        if self._verbose:
            print("GUI.__init__ - initializing GUI ('{}').".format(self._config))

        self._mqtt_client = MQTTClient(self._config["mqtt"], self._verbose)
        self._influxdb_client = MyInfluxDBClient(config["influx"], self._verbose)

        self._state = State()
        self._controller = ControllerManager(config, verbose, self._state, self._mqtt_client)

        elements = ElementFactory.create_elements(self._config["display"]["elements"], self._verbose, self._mqtt_client,
                                                  self._config, self._state)
        self._display = Display(self._config["display"], self._verbose, self._state, elements,
                                self._mqtt_client, self._config["topics-pub"])

        self._stop_loop = threading.Event()
        self._is_stopped = threading.Event()
        self._is_stopped.set()
        self._loop_thread = threading.Thread(target=self._poll_loop)

        if self._verbose:
            print("GUI.__init__ - done.")

    def _calc_sleep_time(self):
        safety = 0.5  # wait n additional seconds
        current_time = time.time()
        seconds_to_next_full_minute = (60 - current_time % 60) + safety  # next full minute in seconds
        if self._verbose:
            print("GUI._calc_sleep_time - seconds to next full minute: '{} s' ({}).".
                  format(seconds_to_next_full_minute, current_time))
        return seconds_to_next_full_minute

    def _poll_loop(self):
        if self._verbose:
            print("GUI._poll_loop - entered poll_loop method.")

        while not self._stop_loop.isSet():
            self._controller.update()
            self._display.update()
            sleep_for = self._calc_sleep_time()
            if self._verbose:
                print("GUI._poll_loop - sleep for " + str(sleep_for) + " seconds.")
            self._stop_loop.wait(sleep_for)

        if self._verbose:
            print("GUI._poll_loop - exiting poll_loop method.")

    def start(self):
        self._is_stopped.clear()
        self._mqtt_client.connect()
        self._mqtt_client.is_connected.wait()
        self._controller.start()
        self._display.start()
        self._loop_thread.start()

    def stop(self):
        self._stop_loop.set()
        self._display.stop()
        self._controller.stop()
        self._loop_thread.join()
        self._mqtt_client.disconnect()
        self._mqtt_client.is_disconnected.wait()
        self._is_stopped.set()

    @classmethod
    def _args_to_config(cls, args=None):
        """Handle command line arguments and read the yaml file into a json structure (=config)."""
        desc = "GUI for thermostat."
        ap = argparse.ArgumentParser(description=desc)
        ap.add_argument('-c', '--config', type=str, help='yaml config file', required=True)
        ap.add_argument('-v', '--verbose', help='verbose', action="store_true")
        ap.add_argument('--version', action='version',
                            version='%(prog)s {}'.format(argaeus.version),
                            help='show the version number and exit')
        if args:
            arguments = vars(ap.parse_args(args))
        else:
            arguments = vars(ap.parse_args())

        verbose = False
        if arguments["verbose"]:
            verbose = True

        config_filename = arguments["config"]
        config_file = Path(config_filename)
        if not config_file.is_file():
            raise FileNotFoundError("config file '{}' not found.".format(config_filename))

        config = mypyyaml.load(open(config_filename, 'r'), Loader=mypyyaml.Loader)

        try:
            credentials_mqtt = mypyyaml.load(open(os.path.expanduser(config["mqtt"]["mqtt-credentials"]), 'r'),
                                        Loader=mypyyaml.Loader)
        except KeyError:
            pass
        else:
            config["mqtt"].update(credentials_mqtt["mqtt"])

        try:
            credentials_influx = mypyyaml.load(open(os.path.expanduser(config["influx"]["influx-credentials"]), 'r'),
                                        Loader=mypyyaml.Loader)
        except KeyError:
            pass
        else:
            config["influx"].update(credentials_influx["influx"])

        return config, verbose

    @classmethod
    def standalone(cls, args=None):
        """Public method to start this driver directly. Instantiates an MQTT client and creates an object for the
                given driver."""
        config, verbose = GUI._args_to_config(args)
        config = mypyyaml.dict_deepcopy_lowercase(config)
        gui = GUI(config, verbose)
        gui.start()
        try:
            while not gui._is_stopped.wait(0.1):  # timeout is necessary for CTRL+C
                pass
        except KeyboardInterrupt:
            pass
        gui.stop()


def standalone():
    GUI.standalone()


if __name__ == "__main__":
    GUI.standalone()
