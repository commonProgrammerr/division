import asyncio
import paho.mqtt.client as mqtt
from division.config.settings import MQTT_HOST, MQTT_PORT


class WatchDog(mqtt.Client):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    async def run(self):
        self.connect(host=MQTT_HOST, port=MQTT_PORT)
        return self.loop_forever()

    def start(self):
        return asyncio.get_event_loop().run_until_complete(self.run())
