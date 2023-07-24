from gate_control import REVERE
from gate_control.__classes__.Switch import Relay
from gate_control.config import RELAYS,DOOR_TRAVEL_TIME,CADENCE,STREAM,CONSUMED

from datetime import datetime as dt
from time import sleep
import argparse

class pigate:

    def __init__(self,MOCK:bool=False) -> None:
        self.MOCK = MOCK
        self.UP = Relay(gpio=RELAYS["GPIO"]["UP"],id='UP')
        self.DN = Relay(gpio=RELAYS["GPIO"]["DN"],id='DN')
        self.door_state = 'DN'
        self.ebrake_active = 0
        self.relays = {'UP':self.UP,'DN':self.DN}
        self.state_msg = {'UP':'Opening','DN':'Closing'}
        self.ts = lambda:dt.now().timestamp()

    # Handle Door Events
    def interrupt(self):
        for relay in self.relays.values():
            relay.open()
        return 'Interrupted'

    def activate(self,relay:Relay):
        if not self.ebrake_active:
            if not self.get_active_relay():
                relay.close()
            return f'{relay.id} Activate'
        else:
            return 'Ebrake is Active, No Actions May Be Taken'

    def toggle_ebrake(self):
        if not self.ebrake_active:
            self.ebrake_active = 1
            for relay in self.relays.values():
                relay.open()
        else: self.ebrake_active = 0
        return {'completion_time':0,'target':'ebrake'}

    def activation_flow(self)->dict:
        active_relay = self.get_active_relay()
        direction = self.get_opposite_direction()
        if active_relay:
            self.interrupt()
            travel = self.travel_time(active_relay.t)
        else:
            travel = DOOR_TRAVEL_TIME
        self.activate(self.relays[direction])
        return {'completion_time':travel + self.ts(),'target':direction}


    def action_wrapper(self,action):
        return {
            'activate':self.activation_flow
            , 'ebrake':self.toggle_ebrake
        }[action]

    def action_triage(self,action):
        triage = [k for k,v in {
            'activate': not self.ebrake_active and action == 'activate'
            ,'ebrake': action == 'ebrake'
        }.items() if v]
        if len(triage) == 1:
            return triage.pop()
        elif len(triage) > 1:
            Exception('Error: Conflicting Events')
        else:
            return


    # Consume and evaluate stream
    def stream_event(self):
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
            events = {x[0]:x[1] for x in events}
            print(events,event)
            todo = self.action_triage(events[event]['action'])
            return self.action_wrapper(todo)()

    def get_relay_states(self)->list:
        return [relay.get_state() for relay in self.relays]

    def get_active_relay(self)->Relay:
        if self.UP.state:
            return self.UP
        elif self.DN.state:
            return self.DN

    def get_opposite_direction(self)->str:
        return {
             'DN':'UP'
            ,'UP':'DN'
            ,'Closing':'UP'
            ,'Opening':'DN'
        }[self.door_state]

    def get_door_motion(self):
        if self.UP.state:
            self.door_state = 'Opening'
        elif self.DN.state:
            self.door_state = 'Closing'
        

    def travel_time(self,start:float):
        t = self.ts()-start
        if t>DOOR_TRAVEL_TIME:
            return DOOR_TRAVEL_TIME
        else: return t

    def set_state(self,):
        REVERE.mset({
            't':dt.now().timestamp()
            ,'state':self.door_state
            ,'ebrake':self.ebrake_active
        })

    def control_flow(self):
        while True:
            self.get_door_motion()
            self.set_state()
            event = self.stream_event()
            if event and event['target'] != 'ebrake':
                if event['completion_time'] >= self.ts():
                    self.interrupt()
                    self.door_state = event['target']
            sleep(CADENCE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--MOCK", type=int, help = "MOCK Status")
    args = parser.parse_args()
    MOCK=args.MOCK
    gate = pigate(MOCK=MOCK)
    gate.control_flow()