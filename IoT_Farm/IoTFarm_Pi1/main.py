import time
from DHT22 import main as main_dht22
from YL69 import main as main_yl69
from WaterSensor import main as main_ws
from PowerPercent import main as main_pp
from Fan import main as main_fan
# import * from water
import requests as rq

# init
watering_flag = False
start = time.time()
res = rq.get("http://140.117.71.98:8000/api/Sensor/sensor1/")
interval = res.json()["interval"]
last = time.time()-5000

while True:
    current = time.time()
    try:
        if current-last >= interval:
            main_dht22()
    except RuntimeError as error:
        print("dht22" , error.args[0])
        print('\n')
    try:
        if (current-last) >= interval:
            main_yl69()
    except RuntimeError as error:
        print("water", error.args[0])
        print('\n')

    try:
        if (current-last)>= interval:
            main_ws()
    except RuntimeError as error:
        print("watersensor" , error.args[0])
        print('\n')
    try:
        if (current-last)>= interval:
            main_pp()
    except RuntimeError as error:
        print("battery", error.args[0])
        print('\n')
    try:
        main_fan()
    except RuntimeError as error:
        print("fan", error.args[0])
        print('\n')
    print("started")
    if (current-last) >= interval:
        last = time.time()
