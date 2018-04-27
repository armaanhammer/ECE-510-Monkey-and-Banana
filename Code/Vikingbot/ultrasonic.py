import time
import RPi.GPIO as GPIO
class Ultrasonic:
        def __init__ (self):
                self.PinTrigger = 21
                self.PinEcho = 20

        def set_Pins(self, pinEcho, pinTrigger):
                self.PinEcho = pinEcho
                self.PinTrigger = pinTrigger
        
        #read the sensor and measure the distance
        def measure(self):
                GPIO.output(self.PinTrigger, True)
                time.sleep(0.00001)
                GPIO.output(self.PinTrigger, False)

                start = time.time()
                while GPIO.input(self.PinEcho) == 0:
                        start = time.time()

                while GPIO.input(self.PinEcho) == 1:
                        stop = time.time()

                elapsed = stop - start
                distance = (elapsed * 34300) / 2

                return distance

        # read the sensor 3 times. measure avarage of 3 distance samples. This function creates a better result. Causes a little bit delay.
        def measure_average(self):
                distance1 = self.measure()
                time.sleep(0.1)
                distance2 = self.measure()
                time.sleep(0.1)
                distance3 = self.measure()
                distance = distance1 + distance2 + distance3
                distance = distance / 3
                return distance

        def setup_GPIO(self):
                GPIO.setup(self.PinTrigger,GPIO.OUT)  # Trigger
                GPIO.setup(self.PinEcho,GPIO.IN)      # Echo
                GPIO.output(self.PinTrigger, False)

        def get_distance(self):
                distance = self.measure_average()
                print "Distance : %.1f" % distance
                return distance
