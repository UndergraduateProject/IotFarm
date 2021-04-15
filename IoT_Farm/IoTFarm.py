import time
import math
import requests as rq
import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # DHT pin to GPIO4

while True:
    humi, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    url = 'http://140.117.71.98:8000/api/humidity/'
    humi = math.floor(humi*100)/100
    temp = math.floor(temp*100)/100
    data = {'value': humi, 'sensorId': temp}
    # data = {'iotHumidity': humi, 'iotTemperature': temp, 'iotSoilMoisture':mois}
    print('溫度:%.2f °C' % temp)
    print('濕度:%.2f ' % humi)
    # print("溫度:{:0.2f}°C".format(temp))  # print格式化後的溫度數值
    # print("濕度:{:0.2f}%".format(humi))  # print格式化後的濕度數值
    # print("土壤濕度:{:0.2f}%".format(mois))  # print格式化後的土壤濕度數值
    res = rq.post(url=url, data=data)
    time.sleep(5)  # delay 59 sec
