import logging
from hubitat import Hubitat

class Mapping:
    def __init__(self, user: str, device: str, tid: str, waypoint: str) -> None:
        self.user = user
        self.device = device
        self.tid = tid
        self.waypoint = waypoint

    def __repr__(self) -> str:
        return f"user={self.user}, device={self.device}, tid={self.tid}, waypoint={self.waypoint}"

# Maps a device/user/tid to a Hubitat device Id
class Mapper:

    def __init__(self, conf: list[dict], hubitat: Hubitat) -> None:
        self._hubitat = hubitat
        self._mapping: dict[str, int] = dict()
        for entry in conf:
            mapping = Mapping(entry['user'], entry['device'], entry['tid'], entry['waypoint'])
            key = str(mapping)
            value = int(entry['hubitatId'])
            if hubitat.has_device(value):
                logging.debug(f"Mapping Owntracks {key} to Hubitat {value}")
                self._mapping[key] = value
            else:
                logging.warn(f"Cannot map Owntracks {key} to Hubitat {value} as device not exposed to MakerAPI")    

    def map(self, m: Mapping, arrived: bool) -> None:
        key: str = str(m)
        id: int = self._mapping.get(k, 0)
        if id:
            logging.info(f"Setting hubitat id {id} to {'arrived' if arrived else 'departed'} for {key}")
            self._hubitat.set_presence(id, arrived)
        else:
            logging.warn(f"No matching hubitat device for user={key}")

