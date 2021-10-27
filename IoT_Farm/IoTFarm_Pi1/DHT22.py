import math
import requests as rq
import adafruit_dht
from board import *
import RPi.GPIO as GPIO
import json

DHT_PIN = D4  # D4  # 自用不用改
DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)
dht22_url = 'http://140.117.71.98:8000/api/Humidtemp/'  # API URL
token_url = 'http://140.117.71.98:8000/user/login/'


def main():
    try:
        dht22_humi = DHT_SENSOR.humidity
        while dht22_humi > 200 or dht22_humi < 0:
            dht22_humi = DHT_SENSOR.humidity
        dht22_humi = math.floor(dht22_humi * 100) / 100
        dht22_temp = DHT_SENSOR.temperature
        while dht22_temp > 50 or dht22_temp < 10:
            dht22_temp = DHT_SENSOR.temperature
        dht22_temp = math.floor(dht22_temp * 100) / 100
        dht22_index = 1  # 幫我刪了 應該用不到
        dht22_data = {'humidity': dht22_humi, 'temperature': dht22_temp, 'heatIndex': dht22_index, 'sensor': "DHT-22"}  # 同上 index應該用不到
        token_url = 'http://140.117.71.98:8000/user/login/'
        token_data = {'username': 'admin', 'password': 'rootroot'}
        res = rq.post(token_url, token_data)
        res = json.loads(res.text)
        headers= {'Authorization': res['token']}
        print('溫度:%.2f°C' % dht22_temp)
        print('濕度:%.2f%%' % dht22_humi)
        res = rq.post(dht22_url, data=dht22_data, headers=headers)
        print(res)
        print('\n')
    except RuntimeError as error:
        print(error.args[0])
        print('\n')


if __name__ == '__main__':
    main()
