import RPi.GPIO as GPIO

SPICLK = 21
SPIMISO = 19
SPIMOSI = 20
SPICS = 16
photo_ch = 0
# API URL


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
        #  rq.post 回傳adc_value(水量)至API
        if adc_value == 0:
            print("no water\n")
        elif 0 < adc_value < 30:
            print("water level:" + str("%.1f" % (adc_value / 200. * 100)) + "%\n")
            print("waterlevel low")
        elif 30 <= adc_value:
            print("water level:" + str("%.1f" % (adc_value / 200. * 100)) + "%\n")
    except RuntimeError as error:
        print(error.args[0])
        print('\n')


if __name__ == '__main__':
    main()

