import smbus
import requests as rq

battery_url = "http://140.117.71.98:8000/api/Electricity/"
# API URL
_REG_CONFIG                 = 0x00
_REG_SHUNTVOLTAGE           = 0x01
_REG_BUSVOLTAGE             = 0x02
_REG_POWER                  = 0x03
_REG_CURRENT                = 0x04
_REG_CALIBRATION            = 0x05

class BusVoltageRange:
    """Constants for ``bus_voltage_range``"""
    RANGE_16V               = 0x00
    RANGE_32V               = 0x01

class Gain:
    """Constants for ``gain``"""
    DIV_1_40MV              = 0x00
    DIV_2_80MV              = 0x01
    DIV_4_160MV             = 0x02
    DIV_8_320MV             = 0x03

class ADCResolution:
    """Constants for ``bus_adc_resolution`` or ``shunt_adc_resolution``"""
    ADCRES_9BIT_1S          = 0x00
    ADCRES_10BIT_1S         = 0x01
    ADCRES_11BIT_1S         = 0x02
    ADCRES_12BIT_1S         = 0x03
    ADCRES_12BIT_2S         = 0x09
    ADCRES_12BIT_4S         = 0x0A
    ADCRES_12BIT_8S         = 0x0B
    ADCRES_12BIT_16S        = 0x0C
    ADCRES_12BIT_32S        = 0x0D
    ADCRES_12BIT_64S        = 0x0E
    ADCRES_12BIT_128S       = 0x0F

class Mode:
    """Constants for ``mode``"""
    POWERDOW                = 0x00      # power down
    SVOLT_TRIGGERED         = 0x01      # shunt voltage triggered
    BVOLT_TRIGGERED         = 0x02      # bus voltage triggered
    SANDBVOLT_TRIGGERED     = 0x03      # shunt and bus voltage triggered
    ADCOFF                  = 0x04      # ADC off
    SVOLT_CONTINUOUS        = 0x05      # shunt voltage continuous
    BVOLT_CONTINUOUS        = 0x06      # bus voltage continuous
    SANDBVOLT_CONTINUOUS    = 0x07      # shunt and bus voltage continuous


class INA219:
    def __init__(self, i2c_bus=1, addr=0x40):
        self.bus = smbus.SMBus(i2c_bus);
        self.addr = addr
        self._cal_value = 0
        self._current_lsb = 0
        self._power_lsb = 0

    def read(self, address):
        data = self.bus.read_i2c_block_data(self.addr, address, 2)
        return ((data[0] * 256 ) + data[1])

    def write(self, address, data):
        temp = [0, 0]
        temp[1] = data & 0xFF
        temp[0] = (data & 0xFF00) >> 8
        self.bus.write_i2c_block_data(self.addr,address,temp)

    def getShuntVoltage_mV(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        value = self.read(_REG_SHUNTVOLTAGE)
        if value > 32767:
            value -= 65535
        return value * 0.01

    def getBusVoltage_V(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        self.read(_REG_BUSVOLTAGE)
        return (self.read(_REG_BUSVOLTAGE) >> 3) * 0.004

    def getCurrent_mA(self):
        value = self.read(_REG_CURRENT)
        if value > 32767:
            value -= 65535
        return value * self._current_lsb

    def getPower_W(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        value = self.read(_REG_POWER)
        if value > 32767:
            value -= 65535
        return value * self._power_lsb


def main():
    ina219 = INA219(addr=0x42)
    try:
        bus_voltage = ina219.getBusVoltage_V()
        p = (bus_voltage - 6) / 2.4 * 100
        if p > 100:
            p = 100
        if p < 0:
            p = 0
        data = {"quantitiy":p, "sensor":"sensor1"}
        headers = {"Authorization" : "Token 5dbb9140a4a995ece1223cbc22343854b7e380f4"}
        res = rq.post(battery_url, data = data, headers = headers)
        print("Power Percent:{:3.1f}%".format(p))
        print("\n")
    except RuntimeError as error:
        print(error.args[0])
        print('\n')


if __name__ == '__main__':
    main()
