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

    servos = createPmod('CON3','JCB')

    try:
        while True:
       
            servos.start()

            print('open')
            servos.set_servo1(50)
            time.sleep(2)

            print('close')
            servos.set_servo1(0)
            time.sleep(2)

            print('neutral')
            servos.set_servo1(50)
            time.sleep(2)
            
            print ('open slowly')
            for i in range(50):
                servos.set_servo1(i)
                time.sleep(.5)

            print('close slowly')
            for i in range(50):
                servos.set_servo1(50 - i)
                time.sleep(.5)

            servos.stop()

    except KeyboardInterrupt:
        pass
    
    finally:
        servos.cleanup() 
