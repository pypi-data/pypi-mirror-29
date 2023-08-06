import collections
import datetime


class GraphData:
    _verbose = None
    slots = None
    MIN = -65536
    MAX = 65536

    def __init__(self, verbose, groups_per_hour):
        self._verbose = verbose
        self.slots = collections.OrderedDict()

        group_by = 60 / groups_per_hour
        for h in range(24):
            for g in range(groups_per_hour):
                key = datetime.time(hour=h, minute=int(g*group_by))
                self.slots[key] = 0

    def fill_history(self, history, entry_name):
        for result in history:
            count = 0
            keys = []  # use instead timestamps of query result
            for k in self.slots.keys():
                keys.append(k)
            for entry in result:
                e = keys[count]
                if self._verbose:
                    print(e, entry)
                value = entry[entry_name]
                if value is not None:
                    self.slots[e] = value
                count = count + 1
                if count >= len(self.slots):
                    count = 0

    def get_min_max_values(self):
        min_value = self.MAX
        max_value = self.MIN
        for value in self.slots.values():
            min_value = min(value, min_value)
            max_value = max(value, max_value)
        return min_value, max_value
