# from flask import Flask, render_template_string, request
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import socketio
import json
import requests as rq
import json

GPIO_pins = (14, 15, 18)  # Microstep Resolution MS1-MS3 -> GPIO Pin
direction = 20  # Direction -> GPIO Pin
step = 21  # Step -> GPIO Pin
url = 'http://140.117.71.98:8000/api/Track/1/'
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
    token_url = 'http://140.117.71.98:8000/user/login/'
    token_data = {'username': 'admin', 'password': 'rootroot'}
    res = rq.post(token_url, token_data)
    res = json.loads(res.text)
    headers= {'Authorization': res['token']}
    if str(direction) == "down":
        if position >= 1000:
            print('Cannot move on')
            print(position)
            sio.emit('slider', "Cannot move on")
        else:
            mymotortest.motor_go(True, "Full", slide, 0.01, False, .05)
            print(position)
            position = position + slide
            data = {'position': position}
            res = rq.patch(url, data)
            sio.emit('slider', "Moving")

    if str(direction) == "up":
        if position <= 0:
            print('Cannot move on')
            print(position)
            sio.emit('slider', "Cannot move on")
        else:
            mymotortest.motor_go(False, "Full", slide, 0.01, False, .05)
            print(position)
            data = {'position': position}
            res = rq.patch(url, data)
            sio.emit('slider', "Moving")


if __name__ == "__main__":
    try:
        sio.connect("http://140.117.71.98:4001")


    except:
        KeyboardInterrupt()
    
    
