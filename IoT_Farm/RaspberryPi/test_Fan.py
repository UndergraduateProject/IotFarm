import RPi.GPIO as GPIO
import time

fan_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_pin, GPIO.OUT)

flag = 0
GPIO.output(fan_pin, flag)

while True:
    # temp = rq.get  # 從DHT22偵測的溫度中獲取
    temp = 30  # 假設
    if temp > 25:
        flag = 1
    else:
        flag = 0
    GPIO.output(fan_pin, flag)
    time.sleep(5)
