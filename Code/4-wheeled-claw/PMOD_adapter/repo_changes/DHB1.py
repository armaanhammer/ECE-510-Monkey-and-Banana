# -*- coding: utf-8 -*-
# Copyright (c) 2017 RS Components Ltd
# SPDX-License-Identifier: MIT License

"""
Interface for PmodHB3 module.
"""

import RPi.GPIO as gpio

CAP = 'GPIO'
PHY = '2x6'
    
STOPPED = 0
FORWARD = 1
REVERSE = -1

class PmodDHB1:

    def __init__(self, DSPMod12):
        
        self.port = DSPMod12
        
        self.en1 = self.port.pin1
        self.dir1 = self.port.pin2
        self.s1A = self.port.pin3
        self.s1B = self.port.pin4
        
        self.en2 = self.port.pin7
        self.dir2 = self.port.pin8
        self.s2A = self.port.pin9
        self.s2B = self.port.pin10

        gpio.setmode(gpio.BCM)

        gpio.setup(self.dir1, gpio.OUT)
        gpio.output(self.dir1, gpio.LOW)
        gpio.setup(self.en1, gpio.OUT)
        
        gpio.setup(self.dir2, gpio.OUT)
        gpio.output(self.dir2, gpio.LOW)
        gpio.setup(self.en2, gpio.OUT)

        gpio.setup(self.s1A, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.s1B, gpio.IN, pull_up_down=gpio.PUD_UP)
        
        gpio.setup(self.s2A, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.s2B, gpio.IN, pull_up_down=gpio.PUD_UP)

        self.enable1 = gpio.PWM(self.en1,100)
        self.enable1.stop()
        
        self.enable2 = gpio.PWM(self.en2,100)
        self.enable2.stop()

        self.direction1 = STOPPED 
        self.direction2 = STOPPED 
        
    def forward(self, duty):
        self.forward1(duty)
        self.forward2(duty)

    def reverse(self, duty):
        self.reverse1(duty)
        self.reverse2(duty)

    def stop(self):
        self.stop1()
        self.stop2()

    def forward1(self,duty):
        if self.direction1 == STOPPED or self.direction1 == FORWARD:
            gpio.output(self.dir1, gpio.HIGH)
            self.enable1.start(0)
            
        else:
            self.enable1.ChangeDutyCycle(0)
            self.enable1.stop()
            gpio.output(self.dir1, gpio.HIGH)
            self.enable1.start(0)
            
        self.enable1.ChangeDutyCycle(duty)    
        self.direction1 = FORWARD
            
    def forward2(self,duty):
        if self.direction2 == STOPPED or self.direction2 == FORWARD:
            gpio.output(self.dir2, gpio.HIGH)
            self.enable2.start(0)
            
        else:
            self.enable2.ChangeDutyCycle(0)
            self.enable2.stop()
            gpio.output(self.dir2, gpio.HIGH)
            self.enable2.start(0)
            
        self.enable2.ChangeDutyCycle(duty)    
        self.direction2 = FORWARD

    def reverse1(self,duty):
        if self.direction1 == STOPPED or self.direction1 == REVERSE:
            gpio.output(self.dir1, gpio.LOW)
            self.enable1.start(0)
            
        else:
            self.enable1.ChangeDutyCycle(0)
            self.enable1.stop()
            gpio.output(self.dir1, gpio.LOW)
            self.enable1.start(0)
            
        self.enable1.ChangeDutyCycle(duty)    
        self.direction1 = REVERSE
        
    def reverse2(self,duty):
        if self.direction2 == STOPPED or self.direction2 == REVERSE:
            gpio.output(self.dir2, gpio.LOW)
            self.enable2.start(0)
            
        else:
            self.enable2.ChangeDutyCycle(0)
            self.enable2.stop()
            gpio.output(self.dir2, gpio.LOW)
            self.enable2.start(0)
            
        self.enable2.ChangeDutyCycle(duty)    
        self.direction2 = REVERSE
        
    def stop1(self):
        self.enable1.ChangeDutyCycle(0)
        self.enable1.stop()
        self.direction1 = STOPPED
        
    def stop2(self):
        self.enable2.ChangeDutyCycle(0)
        self.enable2.stop()
        self.direction2 = STOPPED
        
    def changeFrequency1(self,freq):
        self.enable1.ChangeFrequency(freq)
        
    def changeFrequency2(self,freq):
        self.enable2.ChangeFrequency(freq)
        
    def cleanup(self):
        gpio.cleanup();
        
