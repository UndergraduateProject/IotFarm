import requests as rq
from board import *
import spidev
from numpy import interp
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
spi.open(0, 0)

pump_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)
yl69_url = 'http://140.117.71.98:8000/api/Moisture/'  # API URL
# condition_url = ''  # condition's API route


def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    MCP3008_data = ((adc[1] & 3) << 8) + adc[2]
    return MCP3008_data


def main():
    try:
        mois = analogInput(0)
        mois = interp(mois, [0, 1023], [100, 0])
        mois = int(mois)
        yl69_data = {'moisture': mois}
        print('土壤濕度:%.2f%%' % mois)
        # condition = rq.get  # 從API獲取condition
        if mois > 40:  # 要改condition
            GPIO.output(pump_pin, 0)
            print('不澆水')
        else:
            GPIO.output(pump_pin, 1)
            print('澆水')
        res = rq.post(url=yl69_url, data=yl69_data)
        print(res)
        print('\n')
    except RuntimeError as error:
        print(error.args[0])
        print('\n')


if __name__ == '__main__':
    main()
