import requests as rq
from board import *
import spidev
from numpy import interp
import time
import RPi.GPIO as GPIO

pump_pin = 23  # GPIO23
GPIO.setmode(GPIO.BCM)  # 編碼模式
GPIO.setup(pump_pin, GPIO.OUT)  # 設為輸出口


while True:
    GPIO.output(pump_pin, 1)
    time.sleep(10)
    GPIO.output(pump_pin, 0)
    time.sleep(5)