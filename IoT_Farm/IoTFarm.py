# RaspberryPi先安裝Adafruit_DHT這個Library
# sudo apt-get update
# sudo apt-get install python3-pip
# sudo apt-get install python3-dev python3-pip
# sudo python3 -m pip install --upgrade pip setuptools wheel
# sudo pip3 install Adafruit_DHT

import random
import time
import requests as rq
import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # DHT pin to GPIO4

while True:
    humi, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    # temp = round(random.uniform(20, 40), 2)  # delete
    # humi = round(random.uniform(0, 100), 2)  # delete
    #
    url = 'http://140.117.71.98:8000/api/humidity/'
    data = {'value': humi, 'sensorId': temp}
    # data = {'iotHumidity': humi, 'iotTemperature': temp, 'iotSoilMoisture':mois}
    #round(humi, 2)
    #round(temp, 2)
    
    #humi = (humi*1000)/1000
    
    #print("溫度:{:0.2f}°C".format(temp))  # print格式化後的溫度數值
    #print("濕度:{:0.2f}%".format(humi))  # print格式化後的濕度數值
    print('溫度:%.2f')
    
    # print("土壤濕度:{:0.2f}%".format(mois))  # print格式化後的土壤濕度數值
#     print(type(humi))
#     print(type(temp))
    res = rq.post(url=url, data=data)
    time.sleep(5)  # delay 59 sec
