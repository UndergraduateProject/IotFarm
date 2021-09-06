import time
import math
import requests as rq
import adafruit_dht
from board import *
import spidev
from numpy import interp
import RPi.GPIO as GPIO

# 連結至SPI
spi = spidev.SpiDev()
spi.open(0, 0)

# 設置水泵 & 繼電器
pump_pin = 18  # GPIO18
GPIO.setmode(GPIO.BCM)  # 編碼模式
GPIO.setup(pump_pin, GPIO.OUT)  # 將18號設為輸出口


# 讀取MCP3008的資料
def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    MCP3008_data = ((adc[1] & 3) << 8) + adc[2]
    return MCP3008_data


while True:
    try:
        # YL-69資料讀取
        mois = analogInput(0)  # Reading from CH0
        mois = interp(mois, [0, 1023], [100, 0])
        mois = int(mois)
        # API資料
        yl69_url = 'http://140.117.71.98:8000/api/Moisture/'
        # condition_url = ''
        yl69_data = {'moisture': mois}

        # 輸出
        print('土壤濕度:%.2f%%' % mois)
        # condition = rq.get(url=condition_url)
        # if mois > condition:
        if mois > 40:
            GPIO.output(pump_pin, 0)
            print('不澆水')
        else:
            GPIO.output(pump_pin, 1)
            print('澆水')
        res = rq.post(url=yl69_url, data=yl69_data)  # Post至API
        print(res)
        print('\n')
    except RuntimeError as error:  # 資料讀取失敗時
        print(error.args[0])
        print('\n')
        continue

    time.sleep(5.0)  # delay 5 sec
