from flask import Flask, render_template_string, request 
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction = 20       # Direction -> GPIO Pin
step = 21      # Step -> GPIO Pin

mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

app = Flask(__name__)


TPL = '''
<html>
    <head><title>滑軌控制</title></head>
    <body>
        <form method="POST" action="test">
            <p><input type="range" min="1" max="20" name="slider"/></p>
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
    print(int(slider))
  
    if (int(slider)>10):
       mymotortest.motor_go(True, "Full" , 600,int(slider)*.0004, False, .05)
    
    if (int(slider)<10):
       mymotortest.motor_go(False, "Full" , 600,int(slider)*.001, False, .05)

    return render_template_string(TPL)

if __name__ == "__main__":
    app.run()