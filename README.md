[![GitHub issues](https://img.shields.io/github/issues/vdbg/hubitracks.svg)](https://github.com/vdbg/hubitracks/issues)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/vdbg/hubitracks/main/LICENSE)

# HubiTracks: Hubitat / MQTT Owntracks integration

This program allows for associating [Owntracks](https://owntracks.org/) geofence MQTT updates with [Hubitat](https://hubitat.com/) virtual presence devices.

## Pre-requisites

* [Owntracks](https://owntracks.org/) publishing data to a MQTT broker. See [the booklet](https://owntracks.org/booklet/) to set it up.
* A [Hubitat](https://hubitat.com/) hub.
* A device, capable of running either Docker containers or Python, that is on the same LAN as the hub e.g., [Raspbian](https://www.raspbian.org/) or Windows.
* [Maker API](https://docs.hubitat.com/index.php?title=Maker_API) app installed and configured in Hubitat.
* A `Virtual Presence` device created in Hubitat for each pair of (geofence, owntracks device) that the app should update.
* All of these virtual presence sensors are exported in Maker API.

## Installing

Choose one of these 3 methods.

### Using pre-built Docker image

1. `touch config.toml`
2. This will fail due to malformed config.toml. That's intentional :)
   ``sudo docker run --name my_hubitracks -v "`pwd`/config.toml:/app/config.toml" vdbg/hubitracks``
3. `sudo docker cp my_hubitracks:/app/template.config.toml config.toml`
4. Edit `config.toml` by following the instructions in the file
5. `sudo docker start my_hubitracks -i`
  This will display logging on the command window allowing for rapid troubleshooting. `Ctrl-C` to stop the container if `config.toml` is changed
7. When done testing the config:
  * `sudo docker container rm my_hubitracks`
  * ``sudo docker run -d --name my_hubitracks -v "`pwd`/config.toml:/app/config.toml" --restart=always --memory=100m vdbg/hubitracks``
  * To see logs: `sudo docker container logs -f my_hubitracks`

### Using Docker image built from source

1. `git clone https://github.com/vdbg/hubitracks.git`
2. `sudo docker build -t hubitracks_image hubitracks`
3. `cd hubitracks`
4. `cp template.config.toml config.toml`
5. Edit `config.toml` by following the instructions in the file
6. Test run: ``sudo docker run --name my_hubitracks -v "`pwd`/config.toml:/app/config.toml" hubitracks_image``
   This will display logging on the command window allowing for rapid troubleshooting. `Ctrl-C` to stop the container if `config.toml` is changed
7. If container needs to be restarted for testing: `sudo docker start my_hubitracks -i`
8. When done testing the config:
  * `sudo docker container rm my_hubitracks`
  * ``sudo docker run -d --name my_hubitracks -v "`pwd`/config.toml:/app/config.toml" --restart=always --memory=100m hubitracks_image``
  * To see logs: `sudo docker container logs -f my_hubitracks`

### Running directly on the device

[Python](https://www.python.org/) 3.9 or later with pip3 required.

To install:

1. `git clone https://github.com/vdbg/hubitracks.git`
2. `cd hubitracks`
3. `cp template.config.toml config.toml`
4. Edit `config.toml` by following the instructions in the file
5. `pip3 install -r requirements.txt`
6. Run the program:
  * Interactive mode: `python3 main.py`
  * Shorter: `.\main.py` (Windows) or `./main.py` (any other OS).
  * As a background process (on non-Windows OS): `python3 main.py > log.txt 2>&1 &`
7. To exit: `Ctrl-C` if running in interactive mode, `kill` the process otherwise.

## Troubleshooting

* Set `main:logverbosity` to `DEBUG` in `config.toml` to get more details. Note: **Hubitat's token is printed in plain text** when `main:logverbosity` is `DEBUG`
* Ensure the device running the Python script can access the Hubitat's Maker API by trying to access the `<hubitat:url>/apps/api/<hubitat:appid>/devices?access_token=<hubitat:token>` url from that device (replace placeholders with values from config.toml)

## Authoring

Style:

* From command line: `pip3 install black`,
* In VS code: Settings,
    * Text Editor, Formatting, Format On Save: checked
    * Python, Formatting, Provider: `black`
    * Python, Formatting, Black Args, Add item: `--line-length=200`

## Alternatives

### Life360: nope

Once upon a time, Life360 was a good option for home automation geofencing (as long as you had a high tolerance for
their [shady privacy practices](https://themarkup.org/privacy/2021/12/06/the-popular-family-safety-app-life360-is-selling-precise-location-data-on-its-tens-of-millions-of-user)), but in a textbook bait & switch move they killed the integration APIs used by **all** home automation systems (Hubitat, Home Assistant, ...) in
July 2023 [without notifying anyone](https://community.hubitat.com/t/life360-broken/122202/125), and according to their customer support, intentionally:

> In regards with the Home assistance, please be advised we no longer support home automation programs such as Google Home, Hubitat, Alexa, IFTTT, etc. and Life360 is not compatible with these programs.

### Hubitat app: not really

The built-in support is [unreliable](https://community.hubitat.com/t/android-geofence-not-working/86612), and also means giving way more access than necessary to your Hubitat to folks than needed.

### Hubitat + HTTP Owntracks

That's [a simpler and good alternative](https://community.hubitat.com/t/release-owntracks-presence/53419) to MQTT Owntracks that uses the HTTP Owntracks method.

Pros:
* no need to setup MQTT (e.g. installing [Mosquitto](https://mosquitto.org/) on your server)
* no need for this client (the alternative directly integrates with Hubitat)
* no need to setup MakerAPI


Cons
* Harder to make it work with friends & family. 
* "Loosing" the ability to do more (limited to geofencing, vs. can use the MQTT broker to do other integrations)"
