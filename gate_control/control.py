from gate_control import GPIO
from gate_control.config import SENSORS,RELAYS,DOOR_TRAVEL_TIME,START_STATE,METHOD
from gate_control.__classes__.Sensor import Sense
from gate_control.__classes__.Switch import Relay

from time import sleep
from datetime import datetime as dt

class Gate:
    def __init__(
            self
            ,RELAYS=RELAYS
            ,SENSORS=SENSORS
            ,METHOD=METHOD
            ,START_STATE=START_STATE
            ) -> None:
        self.METHOD = METHOD
        self.last_state = START_STATE
        self.last_activation = dt.now().timestamp()
        self.__relay_meta = RELAYS
        self.__sensor_meta = SENSORS
        self.__initialize_assets__()


    def __initialize_assets__(self):
        self.RELAYS = {x:Relay(gpio=y) for x,y in self.__relay_meta['GPIO'].items()}
        self.SENSORS = {x:Sense(gpio=y) for x,y in self.__sensor_meta['GPIO'].items()}
    
    def __BT_SENSE_STATE__(self):
        return self.SENSORS['BT'].get_state()  

    def __opposite_direction__(self,current_state):
        return {
              'UP':'DN'
            , 'DN':'UP'
            , 'NA':'DN'
        }[current_state]


    def api_activate(self,direction):
        relay = self.RELAYS[direction]
        relay.close()
        sleep(DOOR_TRAVEL_TIME)
        relay.open()


    def activate(self):
        t = dt.now().timestamp()
        tgt = self.__opposite_direction__(self.last_state)
        self.last_state = tgt
        relay = self.RELAYS[tgt]
        relay.close()
        return tgt,t


    def control_flow(self):
        tgt,t = None,dt.now().timestamp()
        active = 0
        while True:
            if (
                self.__BT_SENSE_STATE__()
                and dt.now().timestamp() - t >= 1
                ):
                tgt,t = self.time_activate()
                active = 1
            if (active) and (dt.now().timestamp() - t >= DOOR_TRAVEL_TIME):
                self.RELAYS[tgt].open()
                active = 0
            sleep(SENSORS['PING'])


if __name__ == '__main__':
    Gate().control_flow()   
    GPIO.cleanup()