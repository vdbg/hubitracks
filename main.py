#!/usr/bin/python3

import platform
import sys
import time
import tomllib
import logging


from pathlib import Path
from hubitat import Hubitat
from owntracks import Owntracks
from mapper import Mapper

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_config():
    CONFIG_FILE = "config.toml"
    try:
        with open(Path(__file__).with_name(CONFIG_FILE), "rb") as config_file:
            config = tomllib.load(config_file)

            if not config:
                raise ValueError(f"Invalid {CONFIG_FILE}. See template.{CONFIG_FILE}.")

            for name in {"hubitat", "owntracks", "main", "mapper"}:
                if name not in config:
                    raise ValueError(f"Invalid {CONFIG_FILE}: missing section {name}.")

            return config
    except FileNotFoundError as e:
        logging.error(f"Missing {e.filename}.")
        exit(2)


SUPPORTED_PYTHON_MAJOR = 3
SUPPORTED_PYTHON_MINOR = 11

if sys.version_info < (SUPPORTED_PYTHON_MAJOR, SUPPORTED_PYTHON_MINOR):
    raise Exception(
        f"Python version {SUPPORTED_PYTHON_MAJOR}.{SUPPORTED_PYTHON_MINOR} or later required. Current version: {platform.python_version()}."
    )


try:
    config = get_config()

    main_conf = config["main"]
    logging.getLogger().setLevel(logging.getLevelName(main_conf["log_verbosity"]))

    hubitatConnector = Hubitat(config["hubitat"])
    mapper = Mapper(config["mapper"], hubitatConnector)
    owntracksConnector = Owntracks(config["owntracks"], mapper)

    # blocking call
    owntracksConnector.subscribe()

except Exception as e:
    logging.exception(e)
    exit(1)
