from gate_control import GPIO
from gate_control.config import SENSORS,RELAYS,DOOR_TRAVEL_TIME,START_STATE,METHOD
from gate_control.__classes__.Switch import Relay

from time import sleep
from datetime import datetime as dt

class Gate:
    def __init__(
            self
            ,RELAYS=RELAYS
            ,METHOD=METHOD
            ,START_STATE=START_STATE
            ) -> None:
        self.METHOD = METHOD
        self.last_state = START_STATE
        self.last_activation = dt.now().timestamp()
        self.__relay_meta = RELAYS
        self.__initialize_assets__()

    def _reset_relays(self):
        for relay in self.RELAYS:
            relay.open()

    def __initialize_assets__(self):
        self.RELAYS = {x:Relay(gpio=y) for x,y in self.__relay_meta['GPIO'].items()}

    def __opposite_direction__(self,current_state):
        return {
              'UP':'DN'
            , 'DN':'UP'
            , 'NA':'DN'
        }[current_state]

    def activate(self):
        t = dt.now().timestamp()
        tgt = self.__opposite_direction__(self.last_state)
        self.last_state = tgt
        relay = self.RELAYS[tgt]
        relay.close()
        return tgt,t



if __name__ == '__main__':
    GPIO.cleanup()