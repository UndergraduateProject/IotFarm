import math
import requests as rq
import adafruit_dht
from board import *
import RPi.GPIO as GPIO
import json
import socketio
import json
import operator

DHT_PIN = D4  # D4  # 自用不用改
DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)
dht22_url = 'http://140.117.71.98:8000/api/Humidtemp/'  # API URL
token_url = 'http://140.117.71.98:8000/user/login/'
humidity_url = 'http://140.117.71.98:8000/api/WarningCondition/5/'
temperature_url = 'http://140.117.71.98:8000/api/WarningCondition/6/'
water_url = 'http://140.117.71.98:8000/api/ActionCondition/2/'
fan_url = 'http://140.117.71.98:8000/api/ActionCondition/3/'

sio.connect("http://140.117.71.98:4001")

def water(humid):
    res = rq.get(water_url)  # 從API獲取condition
    conditon = res.json()['humidity']
    status = res.json()['status']
    if humid > conditon or status == 'OFF':  # 要改condition
        GPIO.output(pump_pin, 0)
        print('不澆水')
    else:
        print('澆水')
        GPIO.output(pump_pin, 1)
        time.sleep(5)
        GPIO.output(pump_pin, 0)
        timestamp = time.time()
        msg = {
                'title': 'Automation',
                'body' : 'Watered plant'
            }
        sio.emit('notification', msg)

def fan(temp):
    res = rq.get(fan_url)  # 從API獲取condition
    conditon = res.json()['temperature']
    status = res.json()['status']
    if temp < conditon or status == 'OFF':  # 要改condition
        GPIO.output(pump_pin, 0)
        print('不澆水')
    else:
        print('澆水')
        GPIO.output(pump_pin, 1)
        time.sleep(5)
        GPIO.output(pump_pin, 0)
        timestamp = time.time()
        msg = {
                'title': 'Automation',
                'body' : 'Opened fan'
            }
        sio.emit('notification', msg)


def main():
    try:
        res = rq.get(humidity_url)
        res = res.json()
        humid_cond = res['humidity']
        humid_operator = res['operator']
        res = rq.get(temperature_url)
        res = res.json()
        temp_cond = res['temperature']
        temp_operator = res['operator']

        dht22_humi = DHT_SENSOR.humidity
        dht22_temp = DHT_SENSOR.temperature
        if dht22_humi and dht22_temp :
            while dht22_humi > 200 or dht22_humi < 0:
                dht22_humi = DHT_SENSOR.humidity
            while dht22_temp > 50 or dht22_temp < 10:
                dht22_temp = DHT_SENSOR.temperature
            dht22_humi = math.floor(dht22_humi * 100) / 100
            dht22_temp = math.floor(dht22_temp * 100) / 100
            dht22_index = 1  # 幫我刪了 應該用不到
            water(dht22_humi)
            fan(dht22_temp)
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
            
            if humid_operator == '>':
                if operator.ge(dht22_humi, humid_cond):
                    msg = {
                        'title': 'Warning',
                        'body' : 'Humidity is greater than' + str(humid_cond)
                    }
                    sio.emit('notification', msg)
                
            else:
                if operator.le(dht22_humi, humid_cond):
                    msg = {
                        'title': 'Warning',
                        'body' : 'Humidity is lower than' + str(humid_cond)
                    }
                    sio.emit('notification', msg)

            if temp_operator == '>':
                if operator.ge(dht22_humi, temp_cond):
                    msg = {
                        'title': 'Warning',
                        'body' : 'Temperature is greater than' + str(temp_cond)
                    }
                    sio.emit('notification', msg)
                    
            else:
                if operator.le(dht22_humi, temp_cond):
                    msg = {
                        'title': 'Warning',
                        'body' : 'Temperature is lower than' + str(temp_cond)
                    }
                    sio.emit('notification', msg)

        else:
            print('Error reading value.')

    except RuntimeError as error:
        print(error.args[0])
        print('\n')


if __name__ == '__main__':
    main()
