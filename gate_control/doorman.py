from gate_control import REVERE
from gate_control.__classes__.Switch import Relay
from gate_control.config import RELAYS,DOOR_TRAVEL_TIME,CADENCE

from datetime import datetime
from time import sleep
import argparse

UP = Relay(gpio=RELAYS["GPIO"]["UP"],id='UP')
DN = Relay(gpio=RELAYS["GPIO"]["DN"],id='DN')

relays = {'UP':UP,'DN':DN}
state_msg = {'UP':'Opening','DN':'Closing'}
initial_state = {'task':'DN','t':datetime.now().timestamp(),'state':'DN'}
motion_states = ['Opening','Closing']

def interrupt(relay:Relay,mock:bool):
    if mock:
        return 'Mock Interrupt'
    relay.open()
    return 'Interrupt'

def activate(relay:Relay,mock:bool):
    if mock:
        return 'Mock Activate'
    relay.close()
    return f'{relay.id} Activate'

def control_flow(mock:bool):
    REVERE.mset(initial_state)
    task,t,state = REVERE.mget("task","t","status")
    partial_travel_time = 0
    while True:
        ctask,ct = REVERE.mget("task","t")
        if (ctask,ct) != (task,t):
            print(interrupt(relay=relays[task],mock=mock))
            partial_travel_time = float(ct) - float(t) if state in motion_states else 0
            task,t = ctask,ct
            state = state_msg[task]
            REVERE.set("state",state)
            print(activate(relay=relays[task],mock=mock))
        if (
            datetime.now().timestamp() - float(t) >= (DOOR_TRAVEL_TIME if not partial_travel_time else partial_travel_time)
         ) and (state != task):
            print(interrupt(relay=relays[task],mock=mock))
            state = task
            REVERE.set("state",task)
        sleep(CADENCE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mock", type=int, help = "Mock Status")
    args = parser.parse_args()
    control_flow(mock=args.mock)