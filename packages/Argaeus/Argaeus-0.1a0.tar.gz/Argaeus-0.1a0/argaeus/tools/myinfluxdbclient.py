from influxdb import InfluxDBClient

class MyInfluxDBClient:
    client = None
    _influxdb_username = None
    _influxdb_password = None
    _influxdb_address = None
    _influxdb_port = None
    _influxdb_database = None

    _config = None
    _verbose = None

    def __init__(self, config, verbose):
        self._config = config
        self._verbose = verbose
        if self._verbose:
            print("MyInfluxDBClient.__init__ - creating instance ('{}').".format(self._config))

        self._influxdb_address = str(self._config["influx-address"])
        self._influxdb_port = int(self._config["influx-port"])
        self._influxdb_database = str(self._config["database"])
        self._influxdb_password = str(self._config["influx-password"])
        self._influxdb_username = str(self._config["influx-user"])

        self.client = InfluxDBClient(host=self._influxdb_address, port=self._influxdb_port,
                                       username=self._influxdb_username, password=self._influxdb_password,
                                       database=self._influxdb_database)
