import RPi.GPIO as GPIO
import socketio
import requests as rq


CONTROL_PIN = 17
PWM_FREQ = 50
STEP = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

#socket
sio = socketio.Client()

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle


def switch2deg(deg):
    dc = angle_to_duty_cycle(deg)
    pwm.ChangeDutyCycle(dc)

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("angle")
def on_message(data):
    print('message received with ', data)
    switch2deg(data)
    sio.emit('angle', "camere angle moved")

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


switch2deg(0)
sio.connect()

while True:
    None