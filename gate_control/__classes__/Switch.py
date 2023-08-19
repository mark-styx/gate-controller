from gate_control import GPIO,log
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
        self.state = 0

    def _reset(self):
        log('relay',1,f'\trelay {self.id} reset')
        GPIO.output(self.gpio['OFF'], 0)
        GPIO.output(self.gpio['ON'], 0)
        sleep(PULSE_DELAY)
    
    def _pulse(self,switch):
        log('relay',1,f'pulse {self.id} {switch}')
        self._reset()
        GPIO.output(self.gpio[switch],1)
        sleep(PULSE)
        GPIO.output(self.gpio[switch],0)

    def close(self):
        log('relay',1,'close')
        self._pulse('ON')
        self.t = dt.now().timestamp()
        self.state = 1

    def open(self):
        log('relay',1,'open')
        self._pulse('OFF')
        self.state = 0

    def get_state(self):
        log('relay',1,'get_state')
        return {
             'relay':self.id
            ,'state':self.state
            ,'t':self.t
        }