"""UPS Hat E sensors."""

import logging
import os
import voluptuous as vol

from homeassistant import core
from homeassistant.components.sensor import SensorEntity, PLATFORM_SCHEMA, SensorDeviceClass
# from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
    CONF_NAME,
    CONF_UNIQUE_ID,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import homeassistant.helpers.config_validation as cv

from .coordinator import UpsHatECoordinator

from .const import (
    CONF_ADDR,
    CONF_BATTERY_CAPACITY,
    DEFAULT_ADDR,
    DEFAULT_NAME,
    DEFAULT_UNIQUE_ID,
    LOW_BATTERY_PERCENTAGE,
    CONF_MAX_SOC
)

_LOGGER = logging.getLogger(__name__)

ATTR_CAPACITY = "capacity"
ATTR_SOC = "soc"
ATTR_PSU_VOLTAGE = "psu_voltage"
ATTR_CHARGER_VOLTAGE = "charger_voltage"
ATTR_BATTERY_VOLTAGE = "battery_voltage"
ATTR_BATTERY_CURRENT = "battery_current"
ATTR_CHARGER_CURRENT = "charger_current"
ATTR_POWER = "power"
ATTR_CHARGING = "charging"
ATTR_ONLINE = "online"
ATTR_BATTERY_CONNECTED = "battery_connected"
ATTR_LOW_BATTERY = "low_battery"
ATTR_POWER_CALCULATED = "power_calculated"
ATTR_REMAINING_BATTERY_CAPACITY = "remaining_battery_capacity"
ATTR_REMAINING_TIME = "remaining_time_min"
ATTR_STATE = "state"
ATTR_CELL1_VOLTAGE = "call1_voltage"
ATTR_CELL2_VOLTAGE = "call2_voltage"
ATTR_CELL3_VOLTAGE = "call3_voltage"
ATTR_CELL4_VOLTAGE = "call4_voltage"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_ADDR, default=DEFAULT_ADDR): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_UNIQUE_ID, default=DEFAULT_UNIQUE_ID): cv.string,
    vol.Optional(CONF_BATTERY_CAPACITY, default=4800): cv.positive_int,
    vol.Optional(CONF_MAX_SOC, default=100): cv.positive_int,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Waveshare UPS Hat sensor."""
    name = config.get(CONF_NAME)
    unique_id = config.get(CONF_UNIQUE_ID)
    max_soc = config.get(CONF_MAX_SOC)
    battery_capacity = config.get(CONF_BATTERY_CAPACITY)
    add_entities([UpsHatE(name, unique_id, max_soc, battery_capacity)], True)

class UpsHatE(SensorEntity):
    """Representation of a Waveshare UPS Hat."""
    def __init__(self, name, unique_id=None, max_soc=None, battery_capacity=None):
        """Initialize the sensor."""
        self._name = name
        self._unique_id = unique_id
        if max_soc > 100:
            max_soc = 100
        elif max_soc < 1:
            max_soc = 1
        self._max_soc = max_soc
        self._battery_capacity = battery_capacity
        self._upsHatE = UpsHatECoordinator(addr=0x2d)
        self._attrs = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SensorDeviceClass.BATTERY

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._attrs.get(ATTR_SOC)

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return PERCENTAGE

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._attrs

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return self._unique_id

    def update(self):
        """Get the latest data and update the states."""
        upsHatE = self._upsHatE
        charger_voltage = upsHatE.getChargingVoltage()
        charger_current = upsHatE.getChargingCurrent()
        charger_power = upsHatE.getChargingPower()
        battery_voltage = upsHatE.getBatteryVoltage()
        battery_current = upsHatE.getBatteryCurrent()
        soc = upsHatE.getBatterySOC()
        remaining_battery_capacity = upsHatE.getBatteryRemainingCapacity()
        remaining_time = upsHatE.getBatteryRemainingTime()
        cell1_voltage = upsHatE.getCell1Voltage()
        cell2_voltage = upsHatE.getCell2Voltage()
        cell3_voltage = upsHatE.getCell3Voltage()
        cell4_voltage = upsHatE.getCell4Voltage()
        state = upsHatE.getChargingState()
        online = upsHatE.getOnlineStatus()
        charging = upsHatE.getChargingStatus()
        low_battery = online and soc < LOW_BATTERY_PERCENTAGE
        power_calculated = charger_voltage * (charger_current / 1000)

        self._attrs = {
            ATTR_SOC: round(soc, 0),
            ATTR_CAPACITY: round(soc, 0),
            # ATTR_PSU_VOLTAGE:,
            ATTR_CHARGER_VOLTAGE: round(charger_voltage, 5),
            ATTR_CHARGER_CURRENT: round(charger_current, 5),
            ATTR_BATTERY_VOLTAGE: round(battery_voltage, 5),
            ATTR_BATTERY_CURRENT: round(battery_current, 5),
            ATTR_POWER: round(charger_power, 5),
            ATTR_CHARGING: charging,
            ATTR_ONLINE: online,
            ATTR_LOW_BATTERY: low_battery,
            ATTR_POWER_CALCULATED: round(power_calculated, 5),
            ATTR_REMAINING_BATTERY_CAPACITY: remaining_battery_capacity,
            ATTR_REMAINING_TIME: remaining_time,
            ATTR_STATE: state,
            ATTR_CELL1_VOLTAGE: round(cell1_voltage, 5),
            ATTR_CELL2_VOLTAGE: round(cell2_voltage, 5),
            ATTR_CELL3_VOLTAGE: round(cell3_voltage, 5),
            ATTR_CELL4_VOLTAGE: round(cell4_voltage, 5)
        }
