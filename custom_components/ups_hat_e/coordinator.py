"""UPS Hat E coordinator."""

import logging
import smbus2 as smbus

_LOGGER = logging.getLogger(__name__)


class UpsHatECoordinator():
    def __init__(self, i2c_bus=1, addr=0x2d, battery_capacity=4800):
        """Initialize coordinator."""
        _LOGGER.debug("Initialize coordinator.")
        self._addr = addr
        self._battery_capacity = battery_capacity
        _LOGGER.debug("Assign SMBUS")
        self._bus = smbus.SMBus(i2c_bus)
    
    def read(self, address, block_size):
        _LOGGER.debug(f"read: device addr {self._addr}, register addr {address}, block size {block_size}")
        data = self._bus.read_i2c_block_data(self._addr, address, block_size)
        return (data)
    
    def getChargingState(self):
        data = self.read(0x02, 0x01)
        #_LOGGER.warning(f"Reading data1: {data}")   
        if(data[0] & 0x40):
            state = "Fast Charging"
            _LOGGER.debug("Fast Charging state")
        elif(data[0] & 0x80):
            state = "Charging"
            _LOGGER.debug("Charging state")
        elif(data[0] & 0x20):
            state = "Discharging"
            _LOGGER.debug("Discharge state")
        else:
            state = "Idle"
            _LOGGER.debug("Idle state")
        self._state = state
        return state

    def getChargingVoltage(self):
        data = self.read(0x10, 0x02)
        charger_voltage = (data[0] | data[1] << 8)
        _LOGGER.debug("VBUS Voltage %5dmV"%charger_voltage)
        self._charger_voltage = charger_voltage
        return charger_voltage
    
    def getChargingCurrent(self):
        data = self.read(0x12, 0x02)
        charger_current = (data[0] | data[1] << 8)
        _LOGGER.debug("VBUS Current %5dmA"%charger_current)
        self._charger_current = charger_current
        return charger_current
    
    def getChargingPower(self):
        data = self.read(0x14, 0x02)
        charger_power = (data[0] | data[1] << 8)
        _LOGGER.debug("VBUS Power   %5dmW"%charger_power)
        self._charger_power = charger_power
        return charger_power
    
    def getBatteryVoltage(self):
        data = self.read(0x20, 0x02)
        battery_voltage = (data[0] | data[1] << 8)
        _LOGGER.debug("Battery Voltage %d mV"%battery_voltage)
        self._battery_voltage = battery_voltage
        return battery_voltage
    
    def getBatteryCurrent(self):
        data = self.read(0x22, 0x02)
        battery_current = (data[0] | data[1] << 8)
        if(battery_current > 0x7FFF):
            battery_current -= 0xFFFF
        _LOGGER.debug("Battery Current %d mA"%battery_current)
        self._battery_current = battery_current
        return battery_current
    
    def getBatterySOC(self):
        data = self.read(0x24, 0x02)
        soc = (data[0] | data[1] << 8)
        _LOGGER.debug("Battery Percent %d%%"%soc)
        self._soc = soc
        return soc
    
    def getBatteryRemainingCapacity(self):
        data = self.read(0x26, 0x02)
        remaining_battery_capacity = (data[0] | data[1] << 8)
        _LOGGER.debug("Remaining Capacity %d mAh"%remaining_battery_capacity)
        self._remaining_battery_capacity = remaining_battery_capacity
        return remaining_battery_capacity
   
    def getBatteryRemainingTime(self):
        self._battery_current = self.getBatteryCurrent()
        data = self.read(0x28, 0x04)
        if(self._battery_current < 0):
            remaining_time = (data[0] | data[1] << 8)
            _LOGGER.debug("Run Time To Empty %d min"%remaining_time)
        else:
            remaining_time = (data[2] | data[3] << 8)
            _LOGGER.debug("Average Time To Full %d min"%remaining_time)
        self._remaining_time = remaining_time
        return remaining_time
    
    def getCell1Voltage(self):
        data = self.read(0x30, 0x02)
        cell1_voltage = (data[0] | data[1] << 8)
        _LOGGER.debug("Cell Voltage1 %d mV"%cell1_voltage)
        self._cell1_voltage = cell1_voltage
        return cell1_voltage
    
    def getCell2Voltage(self):
        data = self.read(0x32, 0x02)
        cell2_voltage = (data[0] | data[1] << 8)
        _LOGGER.debug("Cell Voltage2 %d mV"%cell2_voltage)
        self._cell2_voltage = cell2_voltage
        return cell2_voltage
    
    def getCell3Voltage(self):
        data = self.read(0x34, 0x02)
        cell3_voltage = (data[0] | data[1] << 8)
        _LOGGER.debug("Cell Voltage3 %d mV"%cell3_voltage)
        self._cell3_voltage = cell3_voltage
        return cell3_voltage
    
    def getCell4Voltage(self):
        data = self.read(0x36, 0x02)
        cell4_voltage = (data[0] | data[1] << 8)
        _LOGGER.debug("Cell Voltage4 %d mV"%cell4_voltage)
        self._cell4_voltage = cell4_voltage
        return cell4_voltage
    
    def getOnlineStatus(self):
        self._state = self.getChargingState()
        online = bool(self._state != "Discharging")
        self._online = online
        return online
    
    def getChargingStatus(self):
        self._state = self.getChargingState()
        charging = bool(self._state in ["Fast Charging","Charging"])
        self._charging = charging
        return charging