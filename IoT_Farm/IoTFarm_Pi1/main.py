import time
from datetime import datetime, timedelta
from DHT22 import main as main_dht22
from YL69 import main as main_yl69
from WaterSensor import main as main_ws
from PowerPercent import main as main_pp
from Fan import main as main_fan
from Fan import init as init_fan
from water import *
import requests as rq
import RPi.GPIO as GPIO
from LED import *
#import socketio

#sio = socketio.Client()

# init
init_fan()
init_LED()
init_water()

last = False

while True:
    try:
        res = rq.get("http://140.117.71.98:8000/api/Sensor/sensor1/")
        interval = res.json()["interval"]
        interval_hour, interval_minute, interval_second = map(float, interval.split(':'))
        if interval_hour:
            interval = interval_hour
            if last is False:
                last = datetime.now() + timedelta(hours=-interval)
            interval = interval*360

        elif interval_minute:
            interval = interval_minute
            if last is False:
                last = datetime.now() + timedelta(minutes=-interval)
            interval = interval*60

        elif interval_second:
            interval = interval_second
            if last is False :
                last = datetime.now() + timedelta(seconds=-interval)
        current = datetime.now()
        result = str(current-last)
        result_hour, result_minute, result_second = map(float, result.split(':'))
        if interval_hour:
            compare = result_hour*60*60

        elif interval_minute :
            compare = result_minute*60

        elif interval_second:
            compare = result_second
        
        print(interval)
        if compare >= interval:
            last = datetime.now()
            try:
                    main_dht22()
                    print("get dht22")
            except RuntimeError as error:
                print("dht22" , error.args[0])
                print('\n')
            try:
                    main_yl69()
                    print('try watering')
            except RuntimeError as error:
                print("water", error.args[0])
                print('\n')

            try:
                    main_ws()
            except RuntimeError as error:
                print("watersensor" , error.args[0])
                print('\n')
            try:
                    main_pp()
            except RuntimeError as error:
                print("battery", error.args[0])
                print('\n')
            try:
                    main_fan()
            except RuntimeError as error:
                print("fan", error.args[0])
                print('\n')


    except KeyboardInterrupt:
        print("closing")
        GPIO.cleanup()
