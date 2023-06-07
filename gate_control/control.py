from gate_control import GPIO
from gate_control.config import SENSORS,RELAYS
from gate_control.__classes__.Sensor import Sense
from gate_control.__classes__.Switch import Relay

from time import sleep
from datetime import datetime as dt

class Gate:
    def __init__(self,RELAYS=RELAYS,SENSORS=SENSORS) -> None:
        self.last_activation = dt.now().timestamp()
        self.__relay_meta = RELAYS
        self.__sensor_meta = SENSORS
        self.__initialize_assets__()


    def __initialize_assets__(self):
        self.RELAYS = {x:Relay(gpio=y) for x,y in self.__relay_meta['GPIO'].items()}
        self.SENSORS = {x:Sense(gpio=y) for x,y in self.__sensor_meta['GPIO'].items()}

    def __UP_SENSE_STATE__(self):
        return self.SENSORS['UP'].get_state() # depends on NO/NC, assumes NO
    
    def __DN_SENSE_STATE__(self):
        return self.SENSORS['DN'].get_state()
    
    def __BT_SENSE_STATE__(self):
        return self.SENSORS['BT'].get_state()  

    def get_door_state(self):
        if self.__UP_SENSE_STATE__(): return 'UP'
        if self.__DN_SENSE_STATE__(): return 'DN'
        return 'NA'

    def __opposite_direction__(self):
        return {
              'UP':'DN'
            , 'DN':'UP'
            , 'NA':'DN'
        }[self.get_door_state()]


    def activate(self):
        tgt = self.__opposite_direction__()
        relay = self.RELAYS[f'{tgt}']
        relay.close()
        return tgt


    def control_flow(self):
        tgt = None
        while True:
            if self.__BT_SENSE_STATE__():
                t = dt.now().timestamp()
                if t-self.last_activation >= 1:
                    tgt = self.activate()
                    self.last_activation = t
            if self.get_door_state == tgt:
                self.RELAYS[tgt].open()
                tgt == None 
            sleep(self.SENSORS[['PING']])


if __name__ == '__main__':
    Gate().control_flow()   
    GPIO.cleanup()