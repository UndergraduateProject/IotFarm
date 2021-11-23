import RPi.GPIO as GPIO
import requests as rq
import socketio
import json

SPICLK = 21
SPIMISO = 19
SPIMOSI = 20
SPICS = 16
photo_ch = 0
# API URL
water_url = "http://140.117.71.98:8000/api/WaterStorage/"
condition_url = "http://140.117.71.98:8000/api/WarningCondition/7"
sio = socketio.Client()
sio.connect("http://140.117.71.98:4001")

def init():
    GPIO.setwarnings(False)
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)


def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if (adcnum > 7) or (adcnum < 0):
        return -1
    GPIO.output(cspin, True)
    GPIO.output(clockpin, False)
    GPIO.output(cspin, False)
    commandout = adcnum
    commandout |= 0x18
    commandout <<= 3
    for i in range(5):
        if commandout & 0x80:
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
    adcout = 0
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if GPIO.input(misopin):
            adcout |= 0x1
    GPIO.output(cspin, True)
    adcout >>= 1
    return adcout


def main():
    init()
    try:
        adc_value = readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
        res = rq.get(condition_url)
        res = res.json()
        condition = res['volume']
        if adc_value <= condition:
            msg = {
                        'title': 'Warning',
                        'body' : 'Water level is under' + str(condition)
                    }
            sio.emit('notification', msg)
        data = {"volume" : adc_value, sensor:"WaterSensor"}
        token_url = 'http://140.117.71.98:8000/user/login/'
        token_data = {'username': 'admin', 'password': 'rootroot'}
        res = rq.post(token_url, token_data)
        res = json.loads(res.text)
        headers= {'Authorization': 'Token ' + res['token']}
        rq.post(water_url, data = data, headers=headers)
        if adc_value == 0:
            print("no water\n")
        elif 0 < adc_value < 30:
            print("water level:" + str("%.1f" % (adc_value / 200. * 100)) + "%\n")
            print("waterlevel low")
        elif 30 <= adc_value:
            print("water level:" + str("%.1f" % (adc_value / 200. * 100)) + "%\n")
            adc_value = adc_value/200. * 10
            print(adc_value)
        data = {"volume" : adc_value, "sensor" : "WaterSensor"}
        res = rq.post(water_url, data = data, headers = headers) #回傳adc_value(水量)至API
        print(res)

    except RuntimeError as error:
        print(error.args[0])
        print('\n')


if __name__ == '__main__':
    main()

