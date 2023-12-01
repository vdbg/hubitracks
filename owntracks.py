import paho.mqtt.client as mqtt  # https://pypi.org/project/paho-mqtt/
import json
import logging
from hubitat import Hubitat
from mapper import Mapper

# Payloads and topic paths documented in https://owntracks.org/booklet/tech/json/
class Owntracks:
    def __init__(self, conf: dict, mapper: Mapper):
        host: str = conf["host"]
        port: int = int(conf["port"])
        keepalive: int = int(conf["keepalive"])
        user: str = conf["user"]
        password: str = conf["password"]
        logging.info(f"Connecting to MQTT broker {user}@{host}:{port}")
        self._mapper = mapper

        client = mqtt.Client()
        self._client = client
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.username_pw_set(user, password)
        client.enable_logger(logging)
        client.connect(host = host, port = port, keepalive = keepalive)

    def subscribe(self) -> None:
        # Blocking call which processes all network traffic, dispatches
        # callbacks and handles reconnecting.
        self._client.loop_forever()

    # Callback for when the client successfully connects to the broker
    def on_connect(self, client, userdata, flags, reasonCode, properties = None) -> None:
        client.subscribe("owntracks/+/+/event")

    # Callback for when a publish message is received from the broker
    def on_message(self, client, userdata, msg):
        topic = msg.topic

        try:
            data = json.loads(msg.payload)
            logging.debug(f"Payload received: {data}")
            event = data['event'] # enter/leave
            waypoint = data['desc'] # Name of the waypoint
            user_device = topic.split("/") # owntracks/<user>/<device>/event
            user = user_device[1]
            device = user_device[2]
            tid = data['tid']
            self._mapper.map(user, device, tid, waypoint, event == 'enter')
        except Exception as e:
            logging.error(f"Cannot decode data on topic {topic} payload {msg.payload}: {e}")
