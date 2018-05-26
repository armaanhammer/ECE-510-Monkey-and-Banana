#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bring Motors and Servos together for robot
"""
import RPi.GPIO as gpio
from DesignSpark.Pmod.HAT import createPmod
import time

CLAW_OPEN = 50
CLAW_CLOSED = 10

gpio.setwarnings(False)

class ClawRobot:
    def __init__(self, motors1_port, motors2_port, servos_port):
        # Left Motors
        self.motors1 = createPmod('DHB1',motors1_port)

        # Right Motors
        self.motors2 = createPmod('DHB1',motors2_port)

        # Claw
        self.servos = createPmod('CON3',servos_port)

    def open_claw(self):
        self.servos.set_servo1(CLAW_OPEN)

    def close_claw(self):
        self.servos.set_servo1(CLAW_CLOSED)

    def forward(self, delay=2, power=50):
        self.motors1.forward(power)
        self.motors2.forward(power)

        time.sleep(delay)

        self.motors1.stop()
        self.motors2.stop()

    def left(self, delay=2, power=50):
        self.motors1.reverse(power)
        self.motors2.forward(power)

        time.sleep(delay)

        self.motors1.stop()
        self.motors2.stop()

    def right(self, delay=2, power=50):
        self.motors1.forward(power)
        self.motors2.reverse(power)

        time.sleep(delay)

        self.motors1.stop()
        self.motors2.stop()

    def reverse(self, delay=2, power=50):
        self.motors1.reverse(power)
        self.motors2.reverse(power)

        time.sleep(delay)

        self.motors1.stop()
        self.motors2.stop()

    def cleanup(self):
        self.motors1.cleanup()
        self.motors2.cleanup()
        self.servos.cleanup()


if __name__ == '__main__':
    my_robot = ClawRobot(motors1_port='JC', motors2_port='JB', servos_port='JAB')

    for i in range(4):
        print('I am closing my claw')
        my_robot.close_claw()
        time.sleep(2)

        print('I am opening my claw')
        my_robot.open_claw()
        time.sleep(2)

    print('I am closing my claw')
    my_robot.close_claw()

    for i in range(4):
        print('I am going forward for 2 seconds')
        my_robot.forward()
        time.sleep(2)

        print('I am going reverse for 2 seconds')
        my_robot.reverse()
        time.sleep(2)

        print('I am going left for 2 seconds')
        my_robot.left()
        time.sleep(2)

        print('I am going right for 2 seconds')
        my_robot.right()
        time.sleep(2)

    print('I got to the end')

    my_robot.cleanup()
