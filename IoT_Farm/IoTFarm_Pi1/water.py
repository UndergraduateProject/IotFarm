import time
import math
import requests as rq
from board import *
import spidev
from numpy import interp
import socketio
import RPi.GPIO as GPIO
import requests as rq

sio = socketio.Client()
sio.connect("http://140.117.71.98:4001")

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("water")
def on_message(data):
    pump_pin = 12
    print('message received with ', data)
    if str(data["status"]) == "on":
      duration = data["volume"]/50
      GPIO.setup(pump_pin, GPIO.OUT)
      GPIO.output(pump_pin, 1)
      time.sleep(duration)
      print("after sleep")
      GPIO.output(pump_pin, 0)
    
    elif str(data == "off"):
      sio.emit('water', "stopped")
      GPIO.output(pump_pin, 0)

    

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


def init_water():
  # 設置水泵 & 繼電器
  pump_pin = 12  # GPIO23
  GPIO.setmode(GPIO.BCM)  # 編碼模式
  GPIO.setup(pump_pin, GPIO.OUT)  # 設為輸出口
  print("setup GPIO 12")

#socket
#sio = socketio.Client()
#sio.connect("http://140.117.71.98:4001")


if __name__ == "__main__":
  init_water()

