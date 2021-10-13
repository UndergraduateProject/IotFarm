from rpi_ws281x import Adafruit_NeoPixel, Color
import requests as rq
import socketio

sio = socketio.Client()
url = "http://140.117.71.98:8000/api/LED/"
res = rq.get(url)
data = res.json()
count = data['count']
offset = url + str(count)
res = rq.get(offset)
data = res.json()

LED_COUNT = 24
LED_PIN = 18
LED_BRIGHTNESS = 100
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_INVERT = False
RED = int(data['red'])
GREEN = int(data['green'])
BLUE = int(data['blue'])

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)  # 定義

strip.begin()

for i in range(0, strip.numPixels()):
    strip.setPixelColor(i, Color(RED, GREEN, BLUE))  # 更改燈的顏色

strip.show()


@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("light")
def on_message(data):
    print('message received with ', data)
    if data == "cleanup" :
        RED = 0
        GREEN = 0
        BLUE = 0
    else :
        RED = int(data['red'])
        GREEN = int(data['green'])
        BLUE = int(data['blue'])
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(RED, GREEN, BLUE))  # 更改燈的顏色
    strip.show()

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

sio.connect("http://140.117.71.98:4001")

