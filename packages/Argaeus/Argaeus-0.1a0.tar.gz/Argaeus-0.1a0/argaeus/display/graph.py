import datetime
from PIL import ImageDraw
from argaeus.display.aelementmqtt import AElementMQTT
from argaeus.tools.myinfluxdbclient import MyInfluxDBClient
from argaeus.display.graphdata import GraphData


class Graph(AElementMQTT):
    _influx_client = None
    _influx_data_series = None

    _group_by = None  # in minutes. 60 must be a multiple of this value -> 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60
    _pixel_per_slot = None
    _min_degree_per_dot = None # with a height of e.g. 12 dots this value means that the graph will span at least 6
                               # degrees vertically. this min_value prevents that very small temp variants in 24 hours
                               # are equally depicted as huge changes in 24 hours. the 6 degrees in this example should
                               # cover most smart home heating situations.
    _epoch = None
    _epoch_size = None  # group_by as time object
    _next_epoch = None

    _value_buffer = None
    _data = None

    def __init__(self, config_graph, config_influxdb, config_topics_sub, verbose, mqtt_client):
        AElementMQTT.__init__(self, config_graph, config_topics_sub, verbose, mqtt_client)

        try:
            self._influx_data_series = str(config_graph["influx-dataseries"])
        except KeyError:
            if self._verbose:
                print("Graph.__init__ - dont use influxdb.")
            self._influx_data_series = ""

        if len(self._influx_data_series) > 0:
            self._influx_client = MyInfluxDBClient(config_influxdb, verbose)

        if self._width % 24 != 0:
            raise ValueError("Graph - width must be a multiple of 24. ('{}' % 24 != 0)".
                             format(self._width))

        self._group_by = int(self._config["group-by"])
        if 60 % self._group_by != 0:
            raise ValueError("Graph - 60 must be a multiple of group-by. (60 % '{}' != 0)".
                             format(self._group_by))
        self._epoch_size = datetime.time(minute=self._group_by)
        self._epoch = datetime.time()
        self._set_next_epoch()

        groups_per_hour = int(60 / self._group_by)
        pixel_per_hour = int(self._width / 24)
        if pixel_per_hour % groups_per_hour != 0:
            raise ValueError("Graph - width ({}) and group-by ({}) not fulfilling constraint "
                             "'(width / 24) % (60 / group-by) == 0'".format(self._width, self._group_by))
        self._pixel_per_slot = int(pixel_per_hour / groups_per_hour)

        self._min_degree_per_dot = float(self._config["min_degree_per_dot"])

        self._value_buffer = []
        self._data = GraphData(self._verbose, groups_per_hour)

        if self._verbose:
            print("Graph.__init__ - initialized data('{}')".format(self._data.slots.keys()))

    def _set_next_epoch(self):
        current_dt = datetime.datetime.combine(datetime.date(1, 1, 1), self._epoch)
        next_dt = current_dt + datetime.timedelta(minutes=self._epoch_size.minute)
        self._next_epoch = next_dt.time()
        if self._verbose:
            print("Graph._set_next_epoch - next epoch starts at '{}'. current started at '{}'.".
                  format(self._next_epoch, self._epoch))

    def _get_history(self):
        """fill all slots with data from influxdb."""
        if self._verbose:
            print("Graph._get_history - fetching history from influxdb.")

        result = []
        query = "select mean(*) from {} where time>now()-1d group by time({}m)".format(self._influx_data_series,
                                                                                      self._group_by)
        if self._verbose:
            print("Graph._get_history - query-string: '{}'.".format(query))
        query_result = self._influx_client.client.query(query)
        if self._verbose:
            print("Graph._get_history - query-result: '{}'.".format(query_result))
        self._data.fill_history(query_result, "mean_value")
        if self._verbose:
            print("Graph._get_history - slots: '{}'.".format(self._data.slots))

    def _topic_sub_handler(self, value, t=None):  # t for debugging
        if t is None:
            t = datetime.datetime.time(datetime.datetime.now())
        msg_epoch = self._time_to_epoch(t)
        self._value_buffer.append({"time": t, "value": float(value)})
        if self._verbose:
            print("Graph._topic_sub_handle - received value '{}' for epoch '{}'.".format(value, msg_epoch))

        if (msg_epoch >= self._next_epoch) or (msg_epoch < self._epoch):
            # new epoch. second part of if means that current epoch is the last of the day and new epoch is in hour '0'.
            self._set_current_epoch_slot_value()
            if self._verbose:
                print("Graph._topic_sub_handle - new epoch '{}' (old: '{}').".format(msg_epoch, self._epoch))
            self._epoch = msg_epoch  # forward current epoch to msg_epoch
            self._set_next_epoch()

    def _set_current_epoch_slot_value(self):
        value_sum = 0
        count = 0
        if self._verbose:
            print("Graph._set_current_epoch_slot_value - current epoch: '{}'. next epoch starts at '{}'. '{}' values "
                  "in buffer ('{}').".format(self._epoch, self._next_epoch, len(self._value_buffer),
                                             self._value_buffer))
        while True:
            if len(self._value_buffer) == 0:
                if self._verbose:
                    print("Graph._set_current_epoch_slot_value - empty buffer")
                break
            if self._value_buffer[0]["time"] >= self._next_epoch:
                if self._verbose:
                    print("Graph._set_current_epoch_slot_value - buffer contains no more values for this epoch.")
                break
            entry = self._value_buffer.pop(0)
            if self._verbose:
                print("Graph._set_current_epoch_slot_value - popped entry '{}'.".format(entry))
            value_sum = value_sum + entry["value"]
            count = count + 1
        try:
            avg = value_sum / count
        except ZeroDivisionError:
            avg = 0
        self._data.slots[self._epoch] = avg
        if self._verbose:
            print("Graph._set_current_epoch_slot_value - [{}]='{}' (count={}).".format(self._epoch, avg, count))

    def _time_to_epoch(self, t):
        """convert given time to the time object representing its epoch."""
        m = t.minute - (t.minute % self._group_by)
        e = datetime.time(hour=t.hour, minute=m)
        if self._verbose:
            print("Graph._time_to_epoch - {}, {}, {}.".format(t, m, e))
        return e

    def start(self):
        if self._verbose:
            print("Graph.start()")
        self._epoch = self._time_to_epoch(datetime.datetime.time(datetime.datetime.now()))
        if self._influx_client:
            self._get_history()
        pass

    def stop(self):
        if self._verbose:
            print("Graph.stop()")
        pass

    def update_image(self):
        if self._verbose:
            print("Graph.updateImage()")

        min_value, max_value = self._data.get_min_max_values()
        value_per_dot = (max_value - min_value) / (self._height - 1)
        value_per_dot = max(value_per_dot, self._min_degree_per_dot)

        if self._verbose:
            print("Graph.updateImage - min_value: {}, max_value: {}, value_per_dot: {}.".
                  format(min_value, max_value, value_per_dot))

        # clear image
        draw = ImageDraw.Draw(self.img)
        draw.rectangle((0, 0, self._width, self._height), fill=self._background_color)

        # draw graph
        count = 0
        for value in self._data.slots.values():
            x = count * self._pixel_per_slot
            y = self._height - round((value - min_value) / value_per_dot) - 1
            if y < 0:  # rounding may lead to values that are out of bound
                y = 0
            if y >= self._height:  # rounding may lead to values that are out of bound
                y = self._height - 1
            if self._verbose:
                print("Graph.updateImage - value: {}, x: {}, y: {}.".format(value, x, y))
            draw.line(((x, y), (x + self._pixel_per_slot - 1, y)), fill=self._foreground_color)
            count = count + 1

        # draw vertical line for the ongoing epoch
        current_slot = int(self._epoch.hour * 60 + self._epoch.minute) / int(self._epoch_size.minute)
        x = current_slot * self._pixel_per_slot
        if self._verbose:
            print("Graph.updateImage - vertical line: epoch: ({}h, {}m, {}size), slot: {}, x: {}.".
                  format(self._epoch.hour, self._epoch.minute, self._epoch_size, current_slot, x))
        draw.rectangle((x, 0, x + self._pixel_per_slot, self._height), fill=self._foreground_color)

