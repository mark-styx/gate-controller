from gate_control import REVERE
from gate_control.__classes__.Switch import Relay
from gate_control.config import RELAYS,DOOR_TRAVEL_TIME,CADENCE,STREAM,CONSUMED

from datetime import datetime as dt
from time import sleep
import argparse

UP = Relay(gpio=RELAYS["GPIO"]["UP"],id='UP')
DN = Relay(gpio=RELAYS["GPIO"]["DN"],id='DN')

'''
consume events from stream and pass them to consumed queue
handle consumed events gracefully
'''

door_state = 'DN'
ebrake_state = 0
relays = {'UP':UP,'DN':DN}
state_msg = {'UP':'Opening','DN':'Closing'}
ts = lambda:dt.now().timestamp()

# Handle Door Events
def interrupt(relay:Relay):
    if MOCK:
        return 'MOCK Interrupt'
    relay.open()
    return 'Interrupt'

def activate(relay:Relay):
    if MOCK:
        return 'MOCK Activate'
    relay.close()
    return f'{relay.id} Activate'

def ebrake():
    if not ebrake_state:
        ebrake_state = 1
        for relay in relays.values():
            interrupt(relay)
    else: ebrake_state = 0
    return 0

def activation_flow():
    active_relay =  get_active_relay()
    direction = get_opposite_direction()
    door_state = new_door_state(direction)
    if active_relay:
        travel = travel_time(active_relay.get('t'))
        interrupt(relays[active_relay['relay']])
    else:
        travel = DOOR_TRAVEL_TIME
    activate(relays[direction])
    return travel


def action_wrapper(action):
    return {
          'activate':activation_flow
        , 'ebrake':ebrake
    }

def action_triage(action):
    triage = [k for k,v in {
         'activate': not ebrake_state and action == 'activate'
        ,'ebrake': action == 'ebrake'
    }.items() if v]
    if len(triage) == 1:
        return triage.pop()
    elif len(triage) > 1:
        Exception('Error: Conflicting Events')
    else:
        return


# Consume and evaluate stream
def stream_handler():
    events = REVERE.xread(streams={STREAM:0})
    if not events:
        return
    events = events[0][1]
    keys = [k[0] for k in events]
    consumed = REVERE.lrange(CONSUMED,0,REVERE.llen(CONSUMED))
    new_events = [x for x in keys if x not in consumed]
    if new_events:
        event = new_events.pop()
        REVERE.rpush(CONSUMED,event)
        todo = action_triage(events[event]['action'])
        print('triaged',todo)
        complete_time = action_wrapper(todo)()
        return complete_time



def get_relay_states()->list:
    return [relay.state() for relay in relays]

def get_active_relay()->dict:
    R = [x for x in get_relay_states() if x.get('state')]
    if R:
        return R.pop()

def get_opposite_direction()->str:
    return {
         'DN':'UP'
        ,'UP':'DN'
        ,'Closing':'UP'
        ,'Opening':'DN'
    }[door_state]

def new_door_state(direction):
    return {
         'DN':'Closing'
        ,'UP':'Opening'
    }[direction]

def travel_time(start:float):
    return max(DOOR_TRAVEL_TIME/2,(ts()-start))

def set_state():
    REVERE.mset({
        't':dt.now().timestamp()
        ,'state':door_state
        ,'ebrake':ebrake_state
    })

def control_flow():
    while True:
        set_state()
        stream_handler()
        sleep(CADENCE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--MOCK", type=int, help = "MOCK Status")
    args = parser.parse_args()
    MOCK=args.MOCK
    control_flow()