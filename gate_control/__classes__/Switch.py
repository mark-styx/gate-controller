from gate_control import GPIO
from time import sleep

PULSE = 1
DELAY = .5
class Relay:

    def __init__(self,gpio,id) -> None:
        self.id = id
        self.gpio = gpio
        GPIO.setup(self.gpio['ON'], GPIO.OUT)
        GPIO.setup(self.gpio['OFF'], GPIO.OUT)

    def _reset(self):
        print(f'relay {self.id} reset')
        GPIO.output(self.gpio['OFF'], 0)
        GPIO.output(self.gpio['ON'], 0)
        sleep(DELAY)
    
    def _pulse(self,switch):
        print(f'pulse {self.id} {switch}')
        self._reset()
        GPIO.output(self.gpio[switch],1)
        sleep(PULSE)
        GPIO.output(self.gpio[switch],0)

    def close(self):
        self._pulse('ON')

    def open(self):
        self._pulse['OFF']