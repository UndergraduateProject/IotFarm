import RPi.GPIO as GPIO

fan_pin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_pin, GPIO.OUT)
# API URL


def main():
    try:
        # temp = rq.get  # 從DHT22偵測的溫度中獲取
        # condition = rq.get  # 從資料庫取得條件
        temp = 30  # 要修改成從資料庫取得
        if temp > 25:  # 要修改成從資料庫取得條件
            flag = 1
            print('Fan On')
        else:
            flag = 0
            print('Fan Off')
        GPIO.output(fan_pin, flag)
    except RuntimeError as error:
        print(error.args[0])
        print('\n')
