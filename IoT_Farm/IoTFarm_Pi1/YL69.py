import requests as rq
from board import *
import spidev
from numpy import interp
import time
import RPi.GPIO as GPIO
import json
import socketio

spi = spidev.SpiDev()
spi.open(0, 0)

pump_pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)
yl69_url = 'http://140.117.71.98:8000/api/Moisture/'  # API URL
condition_url = 'http://140.117.71.98:8000/api/ActionCondition/1/'  # condition's API route
sio = socketio.Client()
sio.connect("http://140.117.71.98:4001")

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
        status = res.json()['status']
        if mois > conditon or status == 'OFF':  # 要改condition
            GPIO.output(pump_pin, 0)
            print('不澆水')
        else:
            print('澆水')
            GPIO.output(pump_pin, 1)
            time.sleep(2)
            GPIO.output(pump_pin, 0)
            timestamp = time.time()
            msg = {
                        'title': 'Automation',
                        'body' : 'Watered plant'
                    }
            sio.emit('notification', msg)
        token_url = 'http://140.117.71.98:8000/user/login/'
        token_data = {'username': 'admin', 'password': 'rootroot'}
        res = rq.post(token_url, token_data)
        res = json.loads(res.text)
        headers= {'Authorization': 'Token ' + res['token']}
        res = rq.post(url=yl69_url, data=yl69_data, headers=headers)
        print(res)
        time.sleep(10)
        print('\n')
    
    except RuntimeError as error:
        print(error.args[0])
        print('\n')
    

if __name__ == '__main__':
    main()
