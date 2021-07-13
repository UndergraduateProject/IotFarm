import time
import math
import requests as rq
import adafruit_dht
from board import *
import spidev
from numpy import interp
import RPi.GPIO as GPIO

DHT_PIN = D4  # GPIO4
DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)  # 定義DHT_SENSOR為DHT22

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
        # DHT-22資料讀取
        dht22_humi = DHT_SENSOR.humidity
        while dht22_humi > 200 or dht22_humi < 0:
            dht22_humi = DHT_SENSOR.humidity
        dht22_humi = math.floor(dht22_humi * 100) / 100  # 格式化資料至小數點後兩位
        dht22_temp = DHT_SENSOR.temperature
        while dht22_temp > 50 or dht22_temp < 10:
            dht22_temp = DHT_SENSOR.temperature
        dht22_temp = math.floor(dht22_temp * 100) / 100
        dht22_index = 1  # 暫時沒想法處理 先假設1

        # YL-69資料讀取
        mois = analogInput(0)  # Reading from CH0
        mois = interp(mois, [0, 1023], [100, 0])
        mois = int(mois)

        # API資料
        dht22_url = 'http://140.117.71.98:8000/api/Humidtemp/'
        yl69_url = 'http://140.117.71.98:8000/api/Moisture/'
        # condition_url = ''
        dht22_data = {'humidity': dht22_humi, 'temperature': dht22_temp, 'heatIndex': dht22_index}
        yl69_data = {'moisture': mois}

        # 輸出
        print('溫度:%.2f°C' % dht22_temp)  # 格式化
        print('濕度:%.2f%%' % dht22_humi)
        print('土壤濕度:%.2f%%' % mois)
        # condition = rq.get(url=condition_url)
        # if mois > condition:
        if mois > 40:
            GPIO.output(pump_pin, 0)
            print('不澆水')
        else:
            GPIO.output(pump_pin, 1)
            print('澆水')
        res = rq.post(url=dht22_url, data=dht22_data)  # Post至API
        print(res)
        res = rq.post(url=yl69_url, data=yl69_data)  # Post至API
        print(res)
        print('\n')
    except RuntimeError as error:  # 資料讀取失敗時
        print(error.args[0])
        print('\n')
        continue

    time.sleep(5.0)  # delay 5 sec
