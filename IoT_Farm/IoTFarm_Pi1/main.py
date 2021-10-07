import time
from DHT22 import main as main_dht22
from YL69 import main as main_yl69
from WaterSensor import main as main_ws
from PowerPercent import main as main_pp
from Fan import main as main_fan

# init
watering_flag = False

while True:
    try:
        main_dht22()
    except RuntimeError as error:
        print("dht22" , error.args[0])
        print('\n')
    try:
        watering_flag = main_yl69(watering_flag)
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
    print("started")

    time.sleep(1)
