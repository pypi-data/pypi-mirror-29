import collections
import datetime
from argaeus.controller.modes.amode import AMode


class ModeSchedule(AMode):
    schedule_raw = None
    schedule = None

    def __init__(self, config, verbose):
        AMode.__init__(self, config, verbose)
        self.schedule_raw = ModeSchedule._sort_dict(self._config["schedule"])
        self.schedule = collections.OrderedDict()

    @staticmethod
    def _sort_dict(d):
        result = collections.OrderedDict()
        for h in range (0, 24):
            for m in range(0, 60):
                key = "{:02}:{:02}".format(h, m)
                dt = datetime.time(hour=h, minute=m)
                try:
                    result[dt] = d[key]
                except KeyError:
                    pass
        return result

    def map_schedule_modes(self, modes):
        if self._verbose:
            print("ModeSchedule.map_schedule_modes - mapping schedule '{}' to mode '{}'.".
                  format(self.schedule_raw, modes))
        for k,v in self.schedule_raw.items():
            program = modes[v]
            if isinstance(program, ModeSchedule):
                raise ValueError("ModeSchedule.map_schedule_modes -  mode must not be of type ModeSchedule ('{}').".
                                 format(type(program)))
            self.schedule[k] = program

    def get_program_at_time(self, time):  # time as datetime.time instance
        result = None
        for dt, program in self.schedule.items():
            result = program
            if dt > time:
                break
        if self._verbose:
            print("ModeSchedule.get_program_at_time - program '{}' at time '{}'.".format(result.name, time))
        return result
