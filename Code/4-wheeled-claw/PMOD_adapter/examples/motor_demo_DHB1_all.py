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

    motor_front = createPmod('DHB1','JA')
    motor_back = createPmod('DHB1','JB')

    try:
        while True:
        
            # print('fwd')
            # motor_front.forward1(20)
            # motor_back.forward1(20)
            # time.sleep(2)
            # motor_front.stop1()
            # motor_back.stop1()
            # time.sleep(2)
            # print('rev')
            # motor_front.reverse1(20)
            # motor_back.reverse1(20)
            # time.sleep(1)
            # motor_front.stop1()
            # motor_back.stop1()
            # time.sleep(2)
            
            
            print ('ramp up fwd 1')
            for i in range(100):
                motor_front.forward1(i)
                motor_back.forward1(i)
                time.sleep(.1)
            
            print ('ramp down fwd 1')
            for i in range(100):
                motor_front.forward1(100-i)
                motor_back.forward1(100-i)
                time.sleep(.1)
                
            motor_front.stop1()
            motor_back.stop1()
            time.sleep(2)
            
            print ('ramp up fwd 2')
            for i in range(100):
                motor_front.forward2(i)
                motor_back.forward2(i)
                time.sleep(.1)

            print ('ramp down fwd 2')
            for i in range(100):
                motor_front.forward2(100-i)
                motor_back.forward2(100-i)
                time.sleep(.1)
                
            motor_front.stop2()
            motor_back.stop2()
            time.sleep(2)
            
            print ('ramp up rev 1')
            for i in range(100):
                motor_front.reverse1(i)
                motor_back.reverse1(i)
                time.sleep(.1)
            
            print ('ramp down rev 1')
            for i in range(100):
                motor_front.reverse1(100-i)
                motor_back.reverse1(100-i)
                time.sleep(.1)
 
            motor_front.stop1()
            motor_back.stop1()
            time.sleep(2)
            
            print ('ramp up rev 2')
            for i in range(100):
                motor_front.reverse2(i)
                motor_back.reverse2(i)
                time.sleep(.1)
            
            print ('ramp down rev 2')
            for i in range(100):
                motor_front.reverse2(100-i)
                motor_back.reverse2(100-i)
                time.sleep(.1)
 
            motor_front.stop2()
            motor_back.stop2()
            time.sleep(2)
            
            break
       
    except KeyboardInterrupt:
        pass
    
    finally:
        motor_front.cleanup() 
        motor_back.cleanup() 
