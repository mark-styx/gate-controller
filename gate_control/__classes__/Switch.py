from gate_control import GPIO
from time import sleep

PULSE = 1
DELAY = .5
class Relay:

    def __init__(self,gpio) -> None:
        self.gpio = gpio
        GPIO.setup(self.gpio['ON'], GPIO.OUT)
        GPIO.setup(self.gpio['OFF'], GPIO.OUT)

    
    def close(self):
        GPIO.output(self.gpio['OFF'], 0)
        sleep(DELAY)
        GPIO.output(self.gpio['ON'], 1)
        sleep(PULSE)
        GPIO.output(self.gpio['ON'], 0)

    def open(self):
        GPIO.output(self.gpio['ON'], 0)
        sleep(DELAY)
        GPIO.output(self.gpio['OFF'], 1)
        sleep(PULSE)
        GPIO.output(self.gpio['OFF'], 0)