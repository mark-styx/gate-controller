from gate_control import REVERE
from gate_control.config import CADENCE
from gate_control.config import SENSORS
from gate_control.__classes__.Sensor import Sense

from datetime import datetime as dt
from time import sleep
import argparse


Button = Sense(gpio=SENSORS['GPIO']['BT'],id='momentary switch')
ts = lambda:dt.now().timestamp()

def __opposite_direction__(current_state):
   travel = {
        'UP':'DN'
      , 'DN':'UP'
      , 'Opening':'DN'
      , 'Closing':'UP'
   }
   target = travel.get(current_state)
   if not target:
      target = REVERE.get('task')
   return target

def button_control_flow(mock=False):
    '''
    Check the state of the momentary switch at a defined cadence.
    If activated, sends message to the doorman and waits for feedback.
    '''
    hist = []
    t = dt.now().timestamp()
    while True:
        if Button.get_state() and (ts() - t >= 1):
            if mock:
                print('mock button activation')
            else:
                hist.append(1)
                t = ts()
                cstate,ct = REVERE.mget(["state","t"])
                if t - float(ct) < 1:
                    msg = 'Not enough time between requests, ignoring'
                    print(msg)
                else:
                    task = __opposite_direction__(cstate)                    
                    if task:
                        REVERE.mset({"task":task,"t":ts()})
                    else:
                        print('Error: Improper Target')
                        continue
                    while cstate not in ['Opening','Closing']:
                        cstate = REVERE.get("state")
                        sleep(CADENCE)
        elif Button.get_state() and not (ts() - t >= 1):
            if mock:
                print('mock button duplicate activation')
            else:
                hist.append(1)
                msg = 'Not enough time between button senses, ignoring'
                print(msg)
        else:
            hist.append(0)
        hist = hist[:30]   
        if sum(hist) == 30:
            print('triggering ebrake')
            ebrake = REVERE.get('ebrake')
            new = {'ON':'OFF','OFF':'ON'}[ebrake]
            REVERE.mset({'ebrake':new,'ebrake_eid':ts()})
        sleep(SENSORS['PING'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mock", type=int, help = "Mock Status")
    args = parser.parse_args()
    button_control_flow(mock=args.mock)