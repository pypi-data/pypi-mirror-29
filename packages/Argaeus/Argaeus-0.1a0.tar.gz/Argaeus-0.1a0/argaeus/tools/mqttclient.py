import paho.mqtt.client as mqtt
from threading import Event, Lock


class MQTTClient(object):
    """Wrapper for the paho.mqtt.client. Used by ADriver and DeviceManager but can also be used for other purposes."""

    client = None  # holds an instance of paho.mqtt.client.Client
    _config = None  # json configuration
    _verbose_mqttclient = False  # print debugging information if set to yes.
    is_connected = None  # threading.Event - True if connection to mqtt broker has been successfully established.
    is_disconnected = None
    _topic_handler = None
    _lock_client = None

    def __init__(self, config, verbose):
        self._config = config
        self._verbose_mqttclient = verbose
        self.is_connected = Event()
        self.is_connected.clear()
        self.is_disconnected = Event()
        self.is_disconnected.set()
        self.client = mqtt.Client()
        self._topic_handler = {}
        self._lock_client = Lock()

    def connect(self):
        """Connect to the mqtt broker using the provided configuration and on_message function."""
        if self._verbose_mqttclient:
            print("MQTTClient.connect() - Connecting to mqtt.")
        with self._lock_client:
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.username_pw_set(self._config["mqtt-user"], password=self._config["mqtt-password"])
            self.client.connect(self._config["mqtt-address"], self._config["mqtt-port"], 60)
            self.client.loop_start()
            if self.is_connected.wait(30):
                for topic in self._topic_handler.keys():
                    if self._verbose_mqttclient:
                        print("MQTTClient.connect() - subscribe to topic '{}'.".format(topic))
                    self.client.subscribe(topic)
            else:
                raise RuntimeError("MQTTClient.connect - connection to broker could not be established.")

    def disconnect(self):
        """Disconnect from mqtt broker and set is_connected to False."""
        with self._lock_client:
            self.client.disconnect()
            self.is_connected.clear()
            self.is_disconnected.set()

    def _on_connect(self, client, userdata, flags, rc):
        """Return code after trying to connect to mqtt brokder. If successfully connected, is_connected is True."""
        if self._verbose_mqttclient:
            print("MQTTClient._on_connect - Connected with result code " + str(rc))
        if rc == 0:
            self.is_connected.set()
            self.is_disconnected.clear()

    def _on_message(self, client, userdata, msg):
        if self._verbose_mqttclient:
            print("MQTTClient._on_message - received message '{}' on topic '{}'.".format(msg.payload, msg.topic))

        for handler in self._topic_handler[msg.topic]:
            if self._verbose_mqttclient:
                print("MQTTClient._on_message - calling handler '{}'.".format(handler))
            handler(msg.payload)

    def publish(self, topic, msg):
        if self._verbose_mqttclient:
            print("MQTTClient.publish - publishing to topic '{}' the message '{}'.".format(topic, msg))
        if self.is_connected.is_set():
            self.client.publish(topic, msg)
        else:
            raise RuntimeWarning("MQTTClient.publish - trying to publish while not being connected to mqtt broker.")

    def subscribe(self, topic, handler):
        if self._verbose_mqttclient:
            print("MQTTClient.subscribe - subscribing topic '{}' with handler '{}'.".format(topic, handler))
        with self._lock_client:
            try:
                h = self._topic_handler[topic]
                h.append(handler)
            except KeyError:
                self._topic_handler[topic] = [handler,]
            if self.is_connected.is_set():
                if self._verbose_mqttclient:
                    print("MQTTClient.subscribe - activating topic subscription.")
                self.client.subscribe(topic)
            print(self._topic_handler)

    def unsubscribe(self, topic, handler):
        if self._verbose_mqttclient:
            print("MQTTClient.unsubscribe - unsubscribing topic '{}' with handler '{}'.".format(topic, handler))
        with self._lock_client:
            if len(self._topic_handler[topic]) > 1:
                self._topic_handler[topic].remove(handler)
            else:
                del(self._topic_handler[topic])
                self.client.unsubscribe(topic)

    @staticmethod
    def merge(driver, mqtt_client):
        """Utility method - joins a driver instance with an external mqtt-client. Must be called before connecting."""
        driver._mqtt = mqtt_client
        mqtt_client.on_message = driver._on_message