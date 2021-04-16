# 1.啟用樹莓派SPI
# sudo raspi-config
# Interface選項啟用SPI
# 重啟樹莓派(輸入reboot)
# --------------------------------------------------------------------------------
# 2.安裝spidev庫:光啟用SPI介面,樹莓派還是無法讀取YL-69的值,spidev將幫助讀取
# sudo apt-get install git python-dev
# git clone git://github.com/doceme/py-spidev
# cd py-spidev/
# sudo python setup.py install
# --------------------------------------------------------------------------------
# 3.安裝numpy庫:YL-69獲得的值還是電壓值而非土壤溼度百分比
# MCP3008 IC接收到的輸出值是0-0123範圍，需將這些值對映到0-100，以得到百分比
# sudo apt-get install python-numpy

import time
import math
import requests as rq
import Adafruit_DHT

# import spidev

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # DHT pin to GPIO4

# 連結SPI
# spi = spidev.SpiDev()
# spi.open(0, 0)

# 讀取MCP3008的資料
# def analogInput(channel):
#   spi.max_speed_hz = 1350000
#   adc = spi.xfer2([1,(8+channel)<<4,0])
#   data = ((adc[1]&3) << 8) + adc[2]
#   return data

while True:
    humi, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)  # 感測溫溼度
    humi = math.floor(humi * 100) / 100  # 格式化資料至小數點後兩位
    temp = math.floor(temp * 100) / 100
    # mois = analogInput(0)  # Reading from CH0
    # mois = interp(output, [0, 1023], [100, 0])
    # mois = int(output)
    url = 'http://140.117.71.98:8000/api/humidity/'  # API位置
    data = {'value': humi, 'sensorId': temp}  # mois加入後delete
    # data = {'iotHumidity': humi, 'iotTemperature': temp, 'iotSoilMoisture':mois}  # mois加入後加入
    print('溫度:%.2f°C' % temp)  # print格式化後的temp
    print('濕度:%.2f%%' % humi)  # print格式化後的humi
    # print('土壤濕度:%.2f%%' % mois)  # print格式化後的mois
    res = rq.post(url=url, data=data)  # Post至API
    time.sleep(5)  # delay 5 sec
