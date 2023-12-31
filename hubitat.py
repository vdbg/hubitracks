import logging

# https://github.com/danielorf/pyhubitat
from pyhubitat import MakerAPI


class Device:
    def __init__(self, conf: dict) -> None:
        self.name: str = f"'{conf['label']}' ({conf['id']})"
        self.presence: str = None

    def __str__(self) -> str:
        return self.name


class Hubitat:
    def __init__(self, conf: dict):
        hub = f"{conf['url'].rstrip('/')}/apps/api/{conf['appid']}"
        logging.info(f"Connecting to hubitat Maker API app {hub}")
        self._api = MakerAPI(conf["token"], hub)
        self._devices_cache: dict[int, Device] = None

    def has_device(self, id: int) -> bool:
        return id in self._devices_cache

    def get_all_devices(self) -> dict[int, Device]:
        if self._devices_cache is None:
            logging.debug("Refreshing all devices cache")
            self._devices_cache = {
                int(x["id"]): Device(x)
                for x in self._api.list_devices_detailed()
                if x["type"] == "Virtual Presence"
            }
            for device in self._devices_cache.values():
                logging.info(f"Found Hubitat virtual presence device {device}.")

        return self._devices_cache

    def set_presence(self, id: int, arrived: bool) -> None:
        command: str = "arrived" if arrived else "departed"
        device: Device = self._devices_cache[id]
        if command == device.presence:
            logging.debug(f"Presence for {device} hasn't changed.")
            return
        logging.info(f"Sending command {command} to Hubitat device {device}")
        self._api.send_command(id, command)
        device.presence = command
