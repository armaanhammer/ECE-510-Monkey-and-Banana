#!/usr/bin/env python3
import os
from time import sleep

import donkeycar as dk

#import parts
from donkeycar.parts.camera import PiCamera
from donkeycar.parts.actuator import PCA9685, PWMSteering, PWMThrottle


class DK_Simple():
    def __init__(self, cfg):
        #Initialize car
        self.cfg = cfg
        self.cam = PiCamera(resolution=cfg.CAMERA_RESOLUTION)
   
        self.steering_controller = PCA9685(cfg.STEERING_CHANNEL)
        self.steering = PWMSteering(controller=self.steering_controller,
                                    left_pulse=cfg.STEERING_LEFT_PWM, 
                                    right_pulse=cfg.STEERING_RIGHT_PWM)
    
        self.throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL)
        self.throttle = PWMThrottle(controller=self.throttle_controller,
                                    max_pulse=cfg.THROTTLE_FORWARD_PWM,
                                    zero_pulse=cfg.THROTTLE_STOPPED_PWM, 
                                    min_pulse=cfg.THROTTLE_REVERSE_PWM)
    
 
        print("You can now go to <your pi ip address>:8887 to drive your car.")

    def forward(self, delay=1, power=None, angle=None):
        if power == None:
            power = self.cfg.THROTTLE_FORWARD_PWM

        if angle == None:
            angle = self.cfg.STEERING_CENTER_PWM

        self.steering_controller.set_pulse(angle)
        self.throttle_controller.set_pulse(power)
	
        sleep(delay)
        self.throttle_controller.set_pulse(self.cfg.THROTTLE_STOPPED_PWM)
        self.steering_controller.set_pulse(self.cfg.STEERING_CENTER_PWM)

    def reverse(self, delay=1, power=None, angle=None):
        if power == None:
            power = self.cfg.THROTTLE_REVERSE_PWM

        if angle == None:
            angle = self.cfg.STEERING_CENTER_PWM

        self.steering_controller.set_pulse(angle)
        self.throttle_controller.set_pulse(power)
        sleep(0.1)
        self.throttle_controller.set_pulse(self.cfg.THROTTLE_STOPPED_PWM)
        sleep(0.1)
        self.throttle_controller.set_pulse(power)
        sleep(delay)
        self.throttle_controller.set_pulse(self.cfg.THROTTLE_STOPPED_PWM)
        self.steering_controller.set_pulse(self.cfg.STEERING_CENTER_PWM)


def main():
    cfg = dk.load_config(config_path='/home/pi/d2/config.py')

    my_car = DK_Simple(cfg)
    return my_car

if __name__ == '__main__':
    main()    
   
