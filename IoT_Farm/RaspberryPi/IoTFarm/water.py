import time
import math
import requests as rq
# import adafruit_dht
from board import *
import spidev
from numpy import interp
import socketio
import RPi.GPIO as GPIO

# 連結至SPI
spi = spidev.SpiDev()
spi.open(0, 0)

# 設置水泵 & 繼電器
pump_pin = 18  # GPIO18
GPIO.setmode(GPIO.BCM)  # 編碼模式
GPIO.setup(pump_pin, GPIO.OUT)  # 將18號設為輸出口

#socket
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("water")
def on_message(data):
    print('message received with ', data)
    if str(data) == "on":
      # GPIO.output(pump_pin, 1)
      sio.emit('water', "watering")
    
    elif str(data == "off"):
      sio.emit('water', "stopped")
      # GPIO.output(pump_pin, 0)
    

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


while True:
    sio.connect("http://140.117.71.98:4001")
    time.sleep(10)
    sio.disconnect()