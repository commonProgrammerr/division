from .validation import get_access_key_by_value
from division.tasks import WatchDog, mqtt


def watch_dog():
    watch_dog = WatchDog(mqtt.CallbackAPIVersion.VERSION2)
    watch_dog.start()


__all__ = ["watch_dog", "get_access_key_by_value"]
