from gate_control import GPIO
from gate_control.config import PULSE_DELAY,PULSE

from time import sleep
from datetime import datetime as dt

class Relay:

    def __init__(self,gpio,id) -> None:
        self.t = dt.now().timestamp()
        self.id = id
        self.gpio = gpio
        GPIO.setup(self.gpio['ON'], GPIO.OUT)
        GPIO.setup(self.gpio['OFF'], GPIO.OUT)

    def _reset(self):
        print(f'relay {self.id} reset')
        GPIO.output(self.gpio['OFF'], 0)
        GPIO.output(self.gpio['ON'], 0)
        sleep(PULSE_DELAY)
    
    def _pulse(self,switch):
        print(f'pulse {self.id} {switch}')
        self._reset()
        GPIO.output(self.gpio[switch],1)
        sleep(PULSE)
        GPIO.output(self.gpio[switch],0)

    def close(self):
        self._pulse('ON')
        self.t = dt.now().timestamp()

    def open(self):
        self._pulse('OFF')

    def state(self):
        return {
             'relay':self.id
            ,'state':GPIO.input(self.gpio['ON'])
            ,'t':self.t
        }