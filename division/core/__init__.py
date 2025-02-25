from .validation import validate_access_key
from division.tasks import WatchDog, mqtt

__all__ = ["validate_access_key"]


def watch_dog():
    watch_dog = WatchDog(mqtt.CallbackAPIVersion.VERSION2)
    watch_dog.start()
