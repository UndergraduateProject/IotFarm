import requests as rq
from board import *
import spidev
from numpy import interp
import time
import RPi.GPIO as GPIO
import socketio

spi = spidev.SpiDev()
spi.open(0, 0)

pump_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)
yl69_url = 'http://140.117.71.98:8000/api/Moisture/'  # API URL
condition_url = 'http://140.117.71.98:8000/api/ActionCondition/1/'  # condition's API route

#socket
sio = socketio.Client()
sio.connect()

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("water")
def on_message(data):
    print('message received with ', data)
    if str(data) == "on":
      GPIO.output(pump_pin, 1)
      sio.emit('water', "watering")
      time.sleep(sleeptime)
      GPIO.output(pump_pin, 0)
    
    elif str(data == "off"):
      sio.emit('water', "stopped")
      GPIO.output(pump_pin, 0)

    

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    MCP3008_data = ((adc[1] & 3) << 8) + adc[2]
    return MCP3008_data


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
            return (True, timestamp) 
        res = rq.post(url=yl69_url, data=yl69_data)
        print(res)
        print('\n')
        return (True, None) 
    
    except RuntimeError as error:
        print(error.args[0])
        print('\n')
    

if __name__ == '__main__':
    main()
