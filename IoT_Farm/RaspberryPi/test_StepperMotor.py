from flask import Flask, render_template_string, request
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

GPIO_pins = (14, 15, 18)  # Microstep Resolution MS1-MS3 -> GPIO Pin
direction = 20  # Direction -> GPIO Pin
step = 21  # Step -> GPIO Pin
position = 0  # 現在為手動調整
# position = rq.get

mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

app = Flask(__name__)

TPL = '''
<html>
    <head><title>滑軌控制</title></head>
    <body>
        <form method="POST" action="test">
            <p><input type="range" min="1" max="2" name="slider"/></p>
            <input type="submit" value="submit"/>
        </form>
    </body>
</html>
'''


@app.route("/")
def home():
    return render_template_string(TPL)


@app.route("/test", methods=["POST"])
def test():
    slider = request.form["slider"]
    global position
    if int(slider) == 2:
        if position == 10:
            print('Cannot move on')
            print(position)
        else:
            mymotortest.motor_go(True, "Full", 100, 0.01, False, .05)
            position = position + 1
            print(position)
            # rq.post(url = '', data = 'position')

    if int(slider) == 1:
        if position == 0:
            print('Cannot move on')
            print(position)
        else:
            mymotortest.motor_go(False, "Full", 100, 0.01, False, .05)
            position = position - 1
            print(position)
            # rq.post(url = '', data = 'position')

    return render_template_string(TPL)


if __name__ == "__main__":
    app.run()
