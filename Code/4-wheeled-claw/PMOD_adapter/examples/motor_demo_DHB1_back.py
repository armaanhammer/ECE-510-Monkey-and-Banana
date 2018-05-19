#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 RS Components Ltd
# SPDX-License-Identifier: MIT License

"""
Spin motor forwards then backwards.
Ramp speed up and then down in forward direction.
Ramp speed up and then down in reverse direction.
"""

from DesignSpark.Pmod.HAT import createPmod
import time

if __name__ == '__main__':

    motor = createPmod('DHB1','JB')

    try:
        while True:
        
            print('fwd')
            motor.forward1(20)
            time.sleep(2)
            motor.stop1()
            time.sleep(2)
            print('rev')
            motor.reverse1(20)
            time.sleep(1)
            motor.stop1()
            time.sleep(2)
            
            
            print ('ramp up fwd')
            for i in range(100):
                motor.forward1(i)
                time.sleep(.1)
            
            print ('ramp down fwd')
            for i in range(100):
                motor.forward1(100-i)
                time.sleep(.1)
                
            motor.stop1()
            time.sleep(2)
            
            print ('ramp up rev')
            for i in range(100):
                motor.reverse1(i)
                time.sleep(.1)
            
            print ('ramp down rev')
            for i in range(100):
                motor.reverse1(100-i)
                time.sleep(.1)
 
            break
       
    except KeyboardInterrupt:
        pass
    
    finally:
        motor.cleanup() 
