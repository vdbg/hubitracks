import logging
from hubitat import Hubitat

# Maps a device/id
class Mapper:

    def __init__(self, conf: list[dict], hubitat: Hubitat) -> None:
        self._hubitat = hubitat
        self._mapping: dict[str, int] = dict()
        for entry in conf:
            key = self.get_key(entry['user'], entry['device'], entry['waypoint'])
            value = int(entry['hubitatId'])
            if hubitat.has_device(value):
                logging.debug(f"Mapping Owntracks {key} to Hubitat {value}")
                self._mapping[key] = value
            else:
                logging.warn(f"Cannot map Owntracks {key} to Hubitat {value} as device not exposed to MakerAPI")    

    def get_key(self, user: str, device: str, waypoint: str) -> str:
        return f"{user}--{device}--{waypoint}"

    def map(self, user: str, device: str, waypoint: str, arrived: bool) -> None:
        id: int = self._mapping.get(self.get_key(user, device, waypoint), 0)
        if id:
            logging.debug(f"Setting hubitat id {id} to {'arrived' if arrived else 'departed'} for user={user}, device={device}, waypoint={waypoint}")
            self._hubitat.set_presence(id, arrived)
        else:
            logging.debug(f"No matching hubitat device for user={user}, device={device}, waypoint={waypoint}")

