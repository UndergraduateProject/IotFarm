import socketio
import requests as rq
import RPi.GPIO as GPIO
import time

fan_pin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_pin, GPIO.OUT)
    
#flag = 0
#GPIO.output(fan_pin, flag)

#socket
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("fan")
def on_message(data):
    print('message received with ', data)
    sio.emit('fan', "message received")
    global flag
    if data == "ON" :
        flag = 1
    
    elif data == "OFF":
        flag = 0

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

def main():
    #GPIO.setup(fan_pin, GPIO.OUT)
    res = rq.get("http://140.117.71.98:8000/api/ActionCondition/3/")
    temp = res.json()["temperature"]
    mode = res.json()["mode"]
    # 從DHT22偵測的溫度中獲取
    if mode == "default":
        #print("currently in auto mode")
        if temp > 25:
            flag = 1
        else:
            flag = 0
        GPIO.output(fan_pin, flag)
        


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        GPIO.output(fan_pin, 0)

