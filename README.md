


# Waveshare UPS HAT (E) Integration for Home Assistant

This integration allows you to monitor [Waveshare UPS Hat (E)](https://www.waveshare.com/wiki/UPS_HAT_(E)) status in your Home Assistant instance.

<img src="https://www.waveshare.com/w/upload/thumb/7/73/UPS-HAT-E-1.jpg/600px-UPS-HAT-E-1.jpg" width="400" />



## Installation
### HACS
If you use [HACS](https://hacs.xyz/) you can install and update this component.
1. Go into HACS -> CUSTOM REPOSITORIES and add url: https://github.com/azhvan/hacs_ups_hat_e with type "integration"
2. Go to integration, search "ups_hat_e" and click *Install*.


### Manual
Download and unzip or clone this repository and copy `custom_components/ups_hat_e/` to your configuration directory of Home Assistant, e.g. `~/.homeassistant/custom_components/`.

In the end your file structure should look like that:
```
~/.homeassistant/custom_components/ups_hat_e/__init__.py
~/.homeassistant/custom_components/ups_hat_e/binary_sensor.py
~/.homeassistant/custom_components/ups_hat_e/const.py
~/.homeassistant/custom_components/ups_hat_e/coordinator.py
~/.homeassistant/custom_components/ups_hat_e/entity.py
~/.homeassistant/custom_components/ups_hat_e/manifest.json
~/.homeassistant/custom_components/ups_hat_e/sensor.py
```

## Configuration
### Sensor
Create a new sensor entry in your `configuration.yaml` 

```yaml
sensor:
  - platform: ups_hat_e
    name: UPS                    # Optional
    addr: 0x2d                   # Optional
    unique_id: waveshare_ups     # Optional
    scan_interval: 20            # Optional
    battery_capacity: 4800       # Optional
```
Following data can be read:
 - Charger Voltage
 - Charger Current
 - Charger Power
 - Battery Voltage
 - Battery Current
 - Soc
 - Remaining Capacity
 - Remaining Time
 - Cell 1 Voltage
 - Cell 2 Voltage
 - Cell 3 Voltage
 - Cell 4 Voltage
 - Charging Status
 - Online Status

### Binary Sensor
In addition to the  sensor devices, you may also create a device which is simply “on” when the UPS status is online and “off” at all other times.

```yaml
binary_sensor:
  - platform: ups_hat_e
```

## Directions for installing smbus support on Raspberry Pi

### HassOS

To enable i2c in Home Assistant OS System follow this [instruction](https://www.home-assistant.io/common-tasks/os/#enable-i2c) or
use this [addon](https://community.home-assistant.io/t/add-on-hassos-i2c-configurator/264167)

### Home Asisstant Core

Enable I2c interface with the Raspberry Pi configuration utility:

```bash
# pi user environment: Enable i2c interface
$ sudo raspi-config
```

Select `Interfacing options->I2C` choose `<Yes>` and hit `Enter`, then go to `Finish` and you'll be prompted to reboot.

Install dependencies for use the `smbus-cffi` module and enable your `homeassistant` user to join the _i2c_ group:

```bash
# pi user environment: Install i2c dependencies and utilities
$ sudo apt-get install build-essential libi2c-dev i2c-tools python-dev libffi-dev

# pi user environment: Add homeassistant user to the i2c group
$ sudo addgroup homeassistant i2c

# pi user environment: Reboot Raspberry Pi to apply changes
$ sudo reboot
```

#### Check the i2c address of the sensor

After installing `i2c-tools`, a new utility is available to scan the addresses of the connected sensors:

```bash
/usr/sbin/i2cdetect -y 1
```

It will output a table like this:

```text
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- 2d -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

## License
MIT 2026