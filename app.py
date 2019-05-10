from flask import Flask, render_template
from sense_hat import SenseHat
import RPi.GPIO as GPIO
import datetime

app = Flask(__name__)

sense = SenseHat()
sense.set_rotation(180)
sense.clear()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lightBulb = 14
lightBulbSts = GPIO.LOW

GPIO.setup(lightBulb, GPIO.OUT)
GPIO.output(lightBulb, GPIO.LOW)

#sense.show_message("Project")

@app.route("/")
def main():
    templateData = getData()
    return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if (deviceName == 'ledRed') & (action == "on"):
        sense.set_pixel(2,2,(255,0,0))
    if (deviceName == 'ledRed') & (action == "off"):
        sense.set_pixel(2,2,(0,0,0))
    
    if (deviceName == 'ledGreen') & (action == "on"):
        sense.set_pixel(3,3,(0,255,0))
    if (deviceName == 'ledGreen') & (action == "off"):
        sense.set_pixel(3,3,(0,0,0))
        
    if (deviceName == 'ledBlue') & (action == "on"):
        sense.set_pixel(4,4,(0,0,255))
    if (deviceName == 'ledBlue') & (action == "off"):
        sense.set_pixel(4,4,(0,0,0))
        
    if (deviceName == 'lightBulb') & (action == "on"):
        GPIO.output(lightBulb, GPIO.HIGH)
    if (deviceName == 'lightBulb') & (action == "off"):
        GPIO.output(lightBulb, GPIO.LOW)
    
    templateData = getData()
    return render_template('index.html', **templateData)

def getData():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M:%S")
   
    pressure = sense.get_pressure()
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
   
    pressure = round(pressure, 2)
    humidity = round(humidity, 2)
    temperature = round((temperature*1.8 +32), 2)
    
    redledData = getRedLedData()
    greenledData = getGreenLedData()
    blueledData = getBlueLedData()
    lightBulbData = getLightBulbData()
    
    templateData = {
        'title' : 'Final Project - EE-551-WS Engineering Python',
        'time': timeString,
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'ledRed':redledData,
        'ledGreen':greenledData,
        'ledBlue':blueledData,
        'lightBulb': lightBulbData
        }
    return templateData

def getRedLedData():
    redPixel = sense.get_pixel(2,2)
    red_on = redPixel[0]
    if red_on > 200:
        ledRedSts = 'ON'
    if red_on < 200:
        ledRedSts = 'OFF'
    return ledRedSts

def getGreenLedData():
    greenPixel = sense.get_pixel(3,3)
    green_on = greenPixel[1]
    if green_on > 200:
        ledGreenSts = 'ON'
    if green_on < 200:
        ledGreenSts = 'OFF'
    return ledGreenSts

def getBlueLedData():
    bluePixel = sense.get_pixel(4,4)
    blue_on = bluePixel[2]
    if blue_on > 200:
        ledBlueSts = 'ON'
    if blue_on < 200:
        ledBlueSts = 'OFF'
    return ledBlueSts

def getLightBulbData():
    lightBulbStatus = GPIO.input(lightBulb)
    if lightBulbStatus == 1:
        lightBulbSts = 'ON'
    if lightBulbStatus == 0:
        lightBulbSts = 'OFF'
    return lightBulbSts

if __name__ == '__main__':
    #app.run(host = '10.69.188.131')
    app.run()

