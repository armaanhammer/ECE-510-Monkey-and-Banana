# -*- coding: utf-8 -*-
# Copyright (c) 2017 RS Components Ltd
# SPDX-License-Identifier: MIT License

"""
Interface for PmodCON3 module.
"""

import RPi.GPIO as gpio

CAP = 'GPIO'
PHY = '1x6'

class PmodCON3:

    def __init__(self, DSPMod6):
        
        self.port = DSPMod6
        
        self.port1 = self.port.pin1
        self.port2 = self.port.pin2
        self.port3 = self.port.pin3
        self.port4 = self.port.pin4
        
        gpio.setmode(gpio.BCM)
        gpio.setup(self.port1, gpio.OUT)
        gpio.setup(self.port2, gpio.OUT)
        gpio.setup(self.port3, gpio.OUT)
        gpio.setup(self.port4, gpio.OUT)
        
        self.servo1 = gpio.PWM(self.port1, 500)
        self.servo2 = gpio.PWM(self.port2, 500)
        self.servo3 = gpio.PWM(self.port3, 500)
        self.servo4 = gpio.PWM(self.port4, 500)
        
        self.servo1.start(50)
        self.servo2.start(50)
        self.servo3.start(50)
        self.servo4.start(50)
       
    def start(self):
        self.servo1.start(50)
        self.servo2.start(50)
        self.servo3.start(50)
        self.servo4.start(50)

    def set_servo1(self, duty):
        self.servo1.ChangeDutyCycle(duty)
    
    def set_servo2(self, duty):
        self.servo2.ChangeDutyCycle(duty)

    def set_servo3(self, duty):
        self.servo3.ChangeDutyCycle(duty)

    def set_servo4(self, duty):
        self.servo4.ChangeDutyCycle(duty)
        
    def changeFrequency(self,freq):
        self.servo1.ChangeFrequency(freq)
        self.servo2.ChangeFrequency(freq)
        self.servo3.ChangeFrequency(freq)
        self.servo4.ChangeFrequency(freq)

    def stop(self):    
        self.servo1.stop()
        self.servo2.stop()
        self.servo3.stop()
        self.servo4.stop()

    def cleanup(self):
        gpio.cleanup();
        
