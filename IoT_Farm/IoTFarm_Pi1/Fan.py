import socketio
import requests as rq
import RPi.GPIO as GPIO
import time

def init():
    fan_pin = 24
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fan_pin, GPIO.OUT)
    sio = socketio.Client()
    sio.connect("http://140.117.71.98:4001")

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("fan")
def on_message(data):
    GPIO.setup(fan_pin, GPIO.OUT)
    print('message received with ', data)
    sio.emit('fan', "message received")
    global flag
    if data == "ON" :
        GPIO.output(fan_pin, 1)
    elif data == "OFF" or data == "cleanup":
        GPIO.output(fan_pin, 0)

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

def main():
    GPIO.setup(fan_pin, GPIO.OUT)
    print("FAN SETUP")
    res = rq.get("http://140.117.71.98:8000/api/ActionCondition/3/")
    temp = res.json()["temperature"]
    mode = res.json()["mode"]
    # 從DHT22偵測的溫度中獲取
    if mode == "auto":
        #print("currently in auto mode")
        if temp > 25:
            GPIO.output(fan_pin, 1)
            msg = {
                        'title': 'Automation',
                        'body' : 'Fan just turned on'
                    }
            sio.emit('notification', msg)
            print("OPEN FAN")
        else:
            GPIO.output(fan_pin, 0)
            msg = {
                        'title': 'Automation',
                        'body' : 'Fan just turned off'
                    }
            sio.emit('notification', msg)


if __name__ == '__main__':
    try:
        init()
        main()

    except KeyboardInterrupt:
        GPIO.output(fan_pin, 0)

