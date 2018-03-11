import requests
from time import sleep
import RPi.GPIO as GPIO
import threading
import datetime


# These are GPIO variables the PI uses to interface with the drv8825
DIR_PIN = 5  # Direction GPIO Pin
STEP_PIN = 6  # Step GPIO Pin
SLEEP_PIN = 11 # Enable/disable controller
# These are used to interact with the camera
EXPOSE_PIN = 17  # red / green
FOCUS_PIN = 27  # orange / white
# These are used to check the micro switches
SW1 = 3 # Pin used for limit switch
SW2 = 4 # Pin used for limit switch



# Class to enable threading
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)


# Function to calibrate slider position left to right
def startCalibration():
    GPIO.setmode(GPIO.BCM)  # Set board mode to Broadcom standard
    GPIO.setup(DIR_PIN, GPIO.OUT)  # Setup direction pin for drv8825 as output
    GPIO.setup(STEP_PIN, GPIO.OUT)  # Setup step pin for drv8825 as output
    GPIO.setup(SLEEP_PIN, GPIO.OUT)  # Setup sleep pin for drv8825 as output
    GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Read limit switch status
    GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Read limit switch status
    GPIO.output(SLEEP_PIN, True)  # Set to high to turn on controller

    leftCounter = 0  # Number of steps needed to move from current position to left switch
    flag = False
    global trackLen
    trackLen = 0  # Number of steps needed to fully traverse the track
    delay = .0005  # Short time delay between on/off cycles of the stepper driver
    MODE = (13, 19, 26)  # Set resolution of the stepper driver through these three pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)}  # Various step modes pulled from https://www.pololu.com/product/2133
    GPIO.output(MODE, RESOLUTION['1/4'])  # Hard-code a resolution of 1/4 speed.


    while True:
        sw1State = GPIO.input(SW1)  # Define variable to hold state of left limit switch
        sw2State = GPIO.input(SW2)  # Define variable to hold state of right limit switch
        if (sw1State and sw2State) and not flag:  # Switch defaults to True
            GPIO.output(DIR_PIN, 1)
            GPIO.output(STEP_PIN, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP_PIN, GPIO.LOW)
            sleep(delay)
            leftCounter += 1
            continue
        elif not sw1State and not flag:
            print('Left switch triggered')
            flag = True
            continue
        elif sw2State and flag:
            GPIO.output(DIR_PIN, 0)
            GPIO.output(STEP_PIN, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP_PIN, GPIO.LOW)
            sleep(delay)
            trackLen += 1
        elif not sw2State:
            print('Right switch triggered, move to start position')
            GPIO.output(DIR_PIN, 1)
            for x in range(trackLen - 100):
                GPIO.output(STEP_PIN, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP_PIN, GPIO.LOW)
                sleep(delay)
            GPIO.cleanup()
            break


# Function to move slider
def sliderMove(userData):

    # print(userData)
    # [{'direction': 0, 'timeDelay': 5, 'shots': 10, 'status': None, 'id': 1, 'insertTime': '2018-03-11 02:53:33'}]

    # Break passed json data into seperate variables
    dirInput = int(userData[0]['direction'])
    shots = int(userData[0]['shots']) - 1
    timeDelay = int(userData[0]['timeDelay'])
    taskId = int(userData[0]['id'])

    GPIO.setmode(GPIO.BCM)  # Set board mode to Broadcom standard
    GPIO.setup(DIR_PIN, GPIO.OUT)  # Setup direction pin for drv8825 as output
    GPIO.setup(STEP_PIN, GPIO.OUT)  # Setup step pin for drv8825 as output
    GPIO.setup(SLEEP_PIN, GPIO.OUT)  # Setup sleep pin for drv8825 as output
    GPIO.output(DIR_PIN, dirInput)  # Set motor output direction
    GPIO.output(SLEEP_PIN, True)  # Set to high to turn on controller

    stepCount = int((trackLen - 200) / int(shots))
    delay = .0005  # Short time delay between on/off cycles of the stepper driver
    MODE = (13, 19, 26)  # Set resolution of the stepper driver through these three pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)} # Various step modes pulled from https://www.pololu.com/product/2133
    GPIO.output(MODE, RESOLUTION['1/4']) # Hard-code a resolution of 1/4 speed.


    for x in range(shots):
        takePicture()
        for y in range(stepCount):
            GPIO.output(STEP_PIN, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP_PIN, GPIO.LOW)
            sleep(delay)
        sleep(timeDelay)
    sleep(timeInput)
    take_picture()
    GPIO.cleanup() # cleanup in-use pins


# Function to make api call to gather the next task
def main():
    lastTask = requests.get('http://127.0.0.1:5000/nexttask')
    userData = lastTask.json()
    now = datetime.datetime.now() + datetime.timedelta(seconds=60)  # TODO - pass a variable from the webpage to set a start delay.
    if now > datetime.datetime.strptime(lastTask.json()[0]['insertTime'], '%Y-%y-%m %H:%M:%S'):
        #startCalibration()
        sliderMove(userData)
        # threading.Thread(target=startCalibration).start()


if __name__ == '__main__':
    main()