# from flask import Flask, render_template_string, request
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import socketio
import json
import requests as rq

GPIO_pins = (14, 15, 18)  # Microstep Resolution MS1-MS3 -> GPIO Pin
direction = 20  # Direction -> GPIO Pin
step = 21  # Step -> GPIO Pin
position = 0
# slide = 10
url = 'http://140.117.71.98:8000/api/Track/'
res = rq.get(url)
data = res.json()["results"]
position = data[0]['position']

#motor
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

#socket
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on("slider")
def on_message(data):
    print('message received with ', data)
    move(data["slide"],data["direction"])

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

def move(slide, direction):
    global position
    if str(direction) == "down":
        if position >= 1000:
            print('Cannot move on')
            print(position)
            sio.emit('slider', "Cannot move on")
        else:
            mymotortest.motor_go(True, "Full", slide, 0.001, False, .05)
            print(position)
            position = position + slide
            res = rq.patch(url, position)
            sio.emit('slider', "Moving")

    if str(direction) == "up":
        if position <= 0:
            print('Cannot move on')
            print(position)
            sio.emit('slider', "Cannot move on")
        else:
            mymotortest.motor_go(False, "Full", slide, 0.001, False, .05)
            print(position)
            position = position - slide
            res = rq.patch(url, position)
            sio.emit('slider', "Moving")


if __name__ == "__main__":
    try:
        sio.connect("http://140.117.71.98:4001")


    except:
        KeyboardInterrupt()
    
    
