import requests as rq
from board import *
import spidev
from numpy import interp
import time
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
spi.open(0, 0)

pump_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)
yl69_url = 'http://140.117.71.98:8000/api/Moisture/'  # API URL
condition_url = 'http://140.117.71.98:8000/api/ActionCondition/1/'  # condition's API route


def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    MCP3008_data = ((adc[1] & 3) << 8) + adc[2]
    return MCP3008_data

def main():
    try:
        GPIO.setup(pump_pin, GPIO.OUT)
        mois = analogInput(0)
        mois = interp(mois, [0, 1023], [100, 0])
        mois = int(mois)
        yl69_data = {'moisture': mois, 'sensor':"YL-69"}
        print('土壤濕度:%.2f%%' % mois)
        res = rq.get(condition_url)  # 從API獲取condition
        conditon = res.json()['moisture']
        if mois > conditon :  # 要改condition
            GPIO.output(pump_pin, 0)
            print('不澆水')
        else:
            GPIO.output(pump_pin, 1)
            print('澆水')
            time.sleep(3)
            GPIO.output(pump_pin, 0)
            timestamp = time.time()
        headers = {"Authorization" : "Token 5dbb9140a4a995ece1223cbc22343854b7e380f4"}
        res = rq.post(url=yl69_url, data=yl69_data, headers=headers)
        print(res)
        print('\n')
    
    except RuntimeError as error:
        print(error.args[0])
        print('\n')
    

if __name__ == '__main__':
    main()
