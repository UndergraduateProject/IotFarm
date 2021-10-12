import time
import math
import requests as rq
from board import *
import spidev
from numpy import interp
import socketio
import RPi.GPIO as GPIO

# 連結至SPI
spi = spidev.SpiDev()
spi.open(0, 0)

# 設置水泵 & 繼電器
pump_pin = 23  # GPIO23
GPIO.setmode(GPIO.BCM)  # 編碼模式
GPIO.setup(pump_pin, GPIO.OUT)  # 設為輸出口
sleeptime = 1 #rq.get()

#socket
sio = socketio.Client()

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


sio.connect("http://140.117.71.98:4001")
