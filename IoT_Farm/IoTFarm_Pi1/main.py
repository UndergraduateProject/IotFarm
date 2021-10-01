import time
from DHT22 import main as main_dht22
from YL69 import main as main_yl69
from WaterSensor import main as main_ws
from PowerPercent import main as main_pp
from Fan import main as main_fan


while True:
    main_dht22()
    main_yl69()
    main_ws()
    main_pp()
    main_fan()

    time.sleep(5)
