import socketio
import requests as rq
# import RPi.GPIO as GPIO
import time

fan_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_pin, GPIO.OUT)

flag = 0
GPIO.output(fan_pin, flag)

#socket
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("slider")
def on_message(data):
    print('message received with ', data)
    sio.emit('fan', "message received")

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

while True:
    temp = rq.get("http://140.117.71.98:8000/api/ActionCondition/3/")
    print(temp)
    # 從DHT22偵測的溫度中獲取
    temp = 30  # 假設
    if temp > 25:
        flag = 1
    else:
        flag = 0
    GPIO.output(fan_pin, flag)
    time.sleep(5)
