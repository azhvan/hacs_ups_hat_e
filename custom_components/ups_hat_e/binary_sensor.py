"""UPS Hat E binary_sensors."""

# from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
import homeassistant.helpers.config_validation as cv


from .coordinator import UpsHatECoordinator

def setup_platform(
    hass,
    config,
    add_entities,
    discovery_info=None,
):
    """Set up an Online Status binary sensor."""
    add_entities([OnlineStatus(config, {})], True)
    """Set up an Charging Status binary sensor."""
    add_entities([ChargingStatus(config, {})], True)

class OnlineStatus(BinarySensorEntity):
    """Representation of an UPS online status."""

    def __init__(self, config, data):
        """Initialize the UPS online status binary device."""
        self._name = "Online"
        self._upsHatE = UpsHatECoordinator(addr=0x2d)
        self._state = True

    @property
    def name(self):
        """Return the name of the UPS online status sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the device class of the binary sensor."""
        return BinarySensorDeviceClass.PLUG

    @property
    def is_on(self):
        """Return true if the UPS is online, else false."""
        return self._state

    def update(self):
        """Get the status from UPS online status and set this entity's state."""
        self._state = self._upsHatE.getOnlineStatus()

class ChargingStatus(BinarySensorEntity):
    """Representation of an UPS charging status."""

    def __init__(self, config, data):
        """Initialize the UPS charging status binary device."""
        self._name = "Charging"
        self._upsHatE = UpsHatECoordinator(addr=0x2d)
        self._state = True

    @property
    def name(self):
        """Return the name of the UPS charging status sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the device class of the charging sensor."""
        return BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return true if the UPS is charging, else false."""
        return self._state

    def update(self):
        """Get the status from UPS charging status and set this entity's state."""
        self._state = self._upsHatE.getChargingStatus()
