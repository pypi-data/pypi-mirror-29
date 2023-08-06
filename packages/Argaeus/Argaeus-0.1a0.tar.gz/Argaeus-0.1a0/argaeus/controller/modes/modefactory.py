from argaeus.controller.modes.modeprogram import ModeProgram
from argaeus.controller.modes.modeschedule import ModeSchedule
import collections


class ModeFactory:
    @staticmethod
    def create_mode(config, verbose, mqtt_client, config_topics_pub):
        if verbose:
            print("ModeFactory.create_mode - creating mode ('{}').".format(config))
        mode = None

        t = config["type"].lower()
        if t == "program":
            mode = ModeProgram(config, verbose, mqtt_client, config_topics_pub)
        elif t == "schedule":
            mode = ModeSchedule(config, verbose)
        else:
            raise ValueError("ModeFactory.create_mode - unknown type '{}'.".format(t))

        return mode

    @staticmethod
    def create_modes(config, verbose, mqtt_client, config_topics_pub):
        if verbose:
            print("ModeFactory.create_modes - creating modes ('{}').".format(config))

        modes = {}
        modes_selectable = []
        for c in config:
            mode = ModeFactory.create_mode(c, verbose, mqtt_client, config_topics_pub)
            modes[mode.name] = mode
            if mode.selectable:
                modes_selectable.append(mode)
        if verbose:
            print("ModeFactory.create_modes - map_schedule_modes")
        for mode in modes.values():
            if isinstance(mode, ModeSchedule):
                mode.map_schedule_modes(modes)

        return modes, modes_selectable
