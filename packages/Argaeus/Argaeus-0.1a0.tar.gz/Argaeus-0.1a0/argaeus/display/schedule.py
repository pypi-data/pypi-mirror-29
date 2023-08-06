from argaeus.display.aelement import AElement
from PIL import ImageDraw


class Schedule(AElement):
    _config_schedule = None
    _patterns = None
    _pattern_schedule = None
    _group_by = None  # in minutes. 60 must be a multiple of this value -> 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60
    _pixel_per_slot = None  # x-axis
    _pixel_per_dot = None  # y-axis
    _state = None

    def __init__(self, config, verbose, state):
        AElement.__init__(self, config, verbose)
        self._state = state

        self._group_by = int(self._config["group-by"])
        if 60 % self._group_by != 0:
            raise ValueError("Schedule - 60 must be a multiple of group-by. (60 % '{}' != 0)".
                             format(self._group_by))
        groups_per_hour = int(60 / self._group_by)
        pixel_per_hour = int(self._width / 24)
        if pixel_per_hour % groups_per_hour != 0:
            raise ValueError("Schedule - width ({}) and group-by ({}) not fulfilling constraint "
                             "'(width / 24) % (60 / group-by) == 0'".format(self._width, self._group_by))
        self._pixel_per_slot = int(pixel_per_hour / groups_per_hour)

        if self._height % 2 != 0:
            raise ValueError("Schedule - height ({}) must be dividable by 2.".format(self._height))
        self._pixel_per_dot = int(self._height / 2)

        self._patterns = self._config["patterns"]
        self._pattern_schedule = []

    def _get_pattern_schedule(self):
        result = []
        try:
            schedule_items = self._state.current_schedule.items()
            if self._verbose:
                print("Schedule._fill_pattern_schedule - currently active schedule '{}'. (patterns: '{}')".
                      format(self._state.current_schedule, self._patterns))
        except AttributeError:
            if self._verbose:
                print("Schedule._fill_pattern_schedule - currently no schedule active.")
        else:
            for k,v in schedule_items:
                p = self._patterns[v.lower()]
                if self._verbose:
                    print("Schedule._fill_pattern_schedule - [{}]: add pattern {}/{}.".
                          format(k, v, p))
                result.append(p)
        return result

    def start(self):
        if self._verbose:
            print("Schedule.start()")

    def stop(self):
        if self._verbose:
            print("Schedule.stop()")

    def update_image(self):
        if self._verbose:
            print("Schedule.updateImage() - pixel/dot: {}, pixel/slot: {}.".
                  format(self._pixel_per_dot, self._pixel_per_slot))

        pattern_schedule = self._get_pattern_schedule()

        # clear image
        draw = ImageDraw.Draw(self.img)
        draw.rectangle((0, 0, self._width, self._height), fill=self._background_color)
        # draw graph
        count = 0
        for pattern in pattern_schedule:
            if self._verbose:
                print("Schedule.update_image - {}. pattern is {}.".format(count, pattern))
            x_from = count * self._pixel_per_slot
            x_to = x_from + self._pixel_per_slot - 1
            count = count + 1
            if pattern == 0: # nothing is displayed
                continue
            elif pattern == 1: # lower dot
                y_lower = self._height - 1
                y_upper = self._height - self._pixel_per_dot
            elif pattern == 2: # full height
                y_lower = self._height - 1
                y_upper = 0
            elif pattern == 3: # upper dot
                y_lower = self._height - self._pixel_per_dot - 1
                y_upper = 0
            else:
                raise ValueError("Schedule.update_image - unknown value for pattern '{}'.".format(pattern))
            if self._verbose:
                print("Schedule.update_image - rectangle({}/{}-{}/{}).".
                      format(count, pattern, x_from, y_lower, x_to, y_upper))
            draw.rectangle((x_from, y_lower, x_to, y_upper), fill=self._foreground_color)

