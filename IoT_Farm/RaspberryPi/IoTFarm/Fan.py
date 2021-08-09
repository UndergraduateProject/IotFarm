import time
import requests as rq
from board import *
import RPi.GPIO as GPIO

# 設置風扇
fan_pin = 18  # 視GPIO配置更改
GPIO.setmode(GPIO.BCM)  # 編碼模式
GPIO.setup(pump_pin, GPIO.OUT)  # 將18號設為輸出口

dht22_url = ''
condition_url = ''

while True:
    try:
        temp = rq.get(url=dht22_url)
        condition = rq.get(url=condition_url)
        if temp > condition:
            GPIO.output(pump_pin, 1)
    except RuntimeError as error:  # 資料讀取失敗時
        print(error.args[0])
        print('\n')
        continue

    time.sleep(5.0)  # delay 5 sec
