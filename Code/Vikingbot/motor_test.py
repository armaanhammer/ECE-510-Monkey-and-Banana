"""
Basic test program for the Vikingbot.

Original code source from: https://github.com/mlherd/vikingbot
"""

import motor_controller as MC
import ultrasonic as US
import RPi.GPIO as GPIO


#DO setup here
#Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

#Create objects for Vikingbot motor controller and HC-SR04 sensor
vb_motor = MC.MotorController()
HC_sensor = US.Ultrasonic()
HC_sensor.setup_GPIO()

vb_motor.setup_GPIO(1,0)
# setup and start PWM set the dulty cycles to 90
vb_motor.setup_PWM()
vb_motor.start_PWM()
vb_motor.set_motorSpeed(90,90)

# set the delay between motions to 2 seconds
vb_motor.set_SleepTime(2)

GPIO.setmode(GPIO.BCM)
HC_sensor.setup_GPIO()
vb_motor.setup_GPIO(1,0)
#obj_front = HC_sensor.get_distance()
#vb_motor.goBack()
vb_motor.set_SleepTime(1)
vb_motor.goForward()
vb_motor.set_SleepTime(1)
vb_motor.goForward()
vb_motor.set_SleepTime(1)
GPIO.cleanup()
