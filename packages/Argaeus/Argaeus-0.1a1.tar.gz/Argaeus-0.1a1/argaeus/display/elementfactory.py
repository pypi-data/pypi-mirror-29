from argaeus.display.graph import Graph
from argaeus.display.schedule import Schedule
from argaeus.display.modeicon import ModeIcon
from argaeus.display.digitalclock import DigitalClock
from argaeus.display.mqtttext import MQTTText
from argaeus.display.setpointtext import SetPointText
from argaeus.display.statictext import StaticText
from argaeus.display.bar import Bar


class ElementFactory:
    @staticmethod
    def create_element(config_element, verbose, mqtt_client, config, state):
        element = None
        if config_element["active"]:
            if config_element["type"].lower() == "graph":
                element = Graph(config_element, config["influx"], config["topics-sub"], verbose, mqtt_client)
            elif config_element["type"].lower() == "schedule":
                element = Schedule(config_element, verbose, state)
            elif config_element["type"].lower() == "modeicon":
                element = ModeIcon(config_element, verbose, state)
            elif config_element["type"].lower() == "setpointtext":
                element = SetPointText(config_element, verbose, state)
            elif config_element["type"].lower() == "statictext":
                element = StaticText(config_element, verbose)
            elif config_element["type"].lower() == "digitalclock":
                element = DigitalClock(config_element, verbose)
            elif config_element["type"].lower() == "mqtttext":
                element = MQTTText(config_element, config["topics-sub"], verbose, mqtt_client)
            elif config_element["type"].lower() == "bar":
                element = Bar(config_element, config["topics-sub"], verbose, mqtt_client)
            else:
                raise ValueError("ElementFactory.create_element - unknown type '{}'".
                                 format(config_element["type"].lower()))
        else:
            if verbose:
                print("ElementFactory.create_element - skipping inactive element '{}.{}'.".
                      format(config_element["type"].lower(), config_element["name"]))

        return element

    @staticmethod
    def create_elements(config_elements, verbose, mqtt_client=None, config=None, get_current_mode_fct=None):
        element_list = []

        if verbose:
            print("ElementFactory.create_elements - start")

        for config_element in config_elements:
            element = ElementFactory.create_element(config_element, verbose, mqtt_client, config, get_current_mode_fct)
            if element is not None:
                element_list.append(element)

        if verbose:
            print("ElementFactory.create_elements - finished")

        return element_list


