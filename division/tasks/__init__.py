import asyncio
import paho.mqtt.client as mqtt
from division.config import settings
from division.core.validation import get_access_key_by_value
from division.models.constraints import AccessKeyType

from division.utils.logger import get_logger
from logging import WARNING, INFO

log = get_logger("watchdog")


class WatchDog(mqtt.Client):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        # Since we subscribed only for a single channel, reason_code_list contains
        # a single entry
        if reason_code_list[0].is_failure:
            log.warning(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            log.info(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_unsubscribe(self, client, userdata, mid, reason_code_list, properties):
        # Be careful, the reason_code_list is only present in MQTTv5.
        # In MQTTv3 it will always be empty
        if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
            log.info("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
        else:
            log.warning(f"Broker replied with failure: {reason_code_list[0]}")
        client.disconnect()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        log.info(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("open/#")

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
        def validate_user_request(lock_id: str):
            try:
                key = get_access_key_by_value(AccessKeyType.PASSWORD, msg.payload.decode())
                return INFO, f"{lock_id} open by: {str(key.user)}"
            except RuntimeError as e:
                return WARNING, f"{lock_id} access denied: {str(e)}"

        match msg.topic.split("/"):
            case ["open", lock_id]:
                log.log(*validate_user_request(lock_id))
            case _:
                log.info(msg.topic + " " + str(msg.payload))

    async def run(self):
        self.connect(host=settings.MQTT_HOST, port=settings.MQTT_PORT)
        return self.loop_forever()

    def start(self):
        return asyncio.get_event_loop().run_until_complete(self.run())
