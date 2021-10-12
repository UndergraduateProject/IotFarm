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


def main(flag):
    try:
        GPIO.setup(pump_pin, GPIO.OUT)
        mois = analogInput(0)
        mois = interp(mois, [0, 1023], [100, 0])
        mois = int(mois)
        yl69_data = {'moisture': mois}
        print('土壤濕度:%.2f%%' % mois)
        res = rq.get(condition_url)  # 從API獲取condition
        conditon = res.json()['moisture']
        if mois > conditon or flag:  # 要改condition
            GPIO.output(pump_pin, 0)
            print('不澆水')
        else:
            GPIO.output(pump_pin, 1)
            print('澆水')
            time.sleep(3)
            res = rq.post(url=yl69_url, data=yl69_data)
            timestamp = time.time()
        res = rq.post(url=yl69_url, data=yl69_data)
        print(res)
        print('\n')
    
    except RuntimeError as error:
        print(error.args[0])
        print('\n')
    

if __name__ == '__main__':
    main()
