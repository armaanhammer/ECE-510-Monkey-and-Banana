import sys
import time
import RPi.GPIO as GPIO

class MotorController:

        def __init__(self):
                self.PinForwardW1 = 13
                self.PinBackwardW1 = 26
                self.PinForwardW2 =  6
                self.PinBackwardW2 = 5
                self.PinPWM_W1 = 22
                self.PinPWM_W2 = 27
                self.sleeptime = 1
                self.p1 = None
                self.p2 = None

        def set_Pins(self, pin1, pin2, pin3, pin4, pin5, pin6):
                self.PinForwardW1 = pin1
                self.PinBackwardW1 = pin2
                self.PinForwardW2 =  pin3
                self.PinBackwardW2 = pin4
                self.PinPWM_W1 = pin5
                self.PinPWM_W2 = pin6

        def set_SleepTime(self, time):
                self.sleeptime = time

        def setup_GPIO(self, mode, warning):
                if mode == 1:
                        GPIO.setmode(GPIO.BCM)
                else:
                        GPIO.setmode(GPIO.BOARD)

                if warning == 1:
                        GPIO.setwarnings(True)
                else:
                        GPIO.setwarnings(False)

                GPIO.setup(self.PinForwardW1, GPIO.OUT)
                GPIO.setup(self.PinBackwardW1, GPIO.OUT)
                GPIO.setup(self.PinForwardW2, GPIO.OUT)
                GPIO.setup(self.PinBackwardW2, GPIO.OUT)
                GPIO.setup(self.PinPWM_W1, GPIO.OUT)
                GPIO.setup(self.PinPWM_W2, GPIO.OUT)

        def setup_PWM(self):
                self.p1 = GPIO.PWM(self.PinPWM_W1, 100)
                self.p2 = GPIO.PWM(self.PinPWM_W2, 100)

        def start_PWM(self):
                self.p1.start(0)
                self.p2.start(0)

        def set_motorSpeed(self, speedW1, speedW2):
                self.p1.ChangeDutyCycle(speedW1)
                self.p2.ChangeDutyCycle(speedW2)
                
        def turnRight(self):
                GPIO.output(self.PinForwardW1, GPIO.HIGH)
                GPIO.output(self.PinBackwardW1, GPIO.LOW)
                GPIO.output(self.PinBackwardW2, GPIO.HIGH)
                GPIO.output(self.PinForwardW2, GPIO.LOW)
                print "turning right"
                time.sleep(self.sleeptime)
                GPIO.output(self.PinForwardW1, GPIO.LOW)
                GPIO.output(self.PinBackwardW2, GPIO.LOW)

        def turnLeft(self):
                GPIO.output(self.PinForwardW1, GPIO.LOW)
                GPIO.output(self.PinBackwardW1, GPIO.HIGH)
                GPIO.output(self.PinForwardW2, GPIO.HIGH)
                GPIO.output(self.PinBackwardW2, GPIO.LOW)
                print "turning left"
                time.sleep(self.sleeptime)
                GPIO.output(self.PinBackwardW1, GPIO.LOW)
                GPIO.output(self.PinForwardW2, GPIO.LOW)

        def goForward(self):
                GPIO.output(self.PinForwardW1, GPIO.HIGH)
                GPIO.output(self.PinForwardW2, GPIO.HIGH)
                GPIO.output(self.PinBackwardW1, GPIO.LOW)
                GPIO.output(self.PinBackwardW2, GPIO.LOW)
                print "going forward"
                time.sleep(self.sleeptime)
                GPIO.output(self.PinForwardW1, GPIO.LOW)
                GPIO.output(self.PinForwardW2, GPIO.LOW)

        def goBack(self):
                GPIO.output(self.PinBackwardW1, GPIO.HIGH)
                GPIO.output(self.PinBackwardW2, GPIO.HIGH)
                GPIO.output(self.PinForwardW1, GPIO.LOW)
                GPIO.output(self.PinForwardW2, GPIO.LOW)
                print "going back"
                time.sleep(self.sleeptime)
                GPIO.output(self.PinBackwardW1, GPIO.LOW)
                GPIO.output(self.PinBackwardW2, GPIO.LOW)

        def cleanup(self):
                GPIO.cleanup()
