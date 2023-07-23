from gate_control import REVERE
from gate_control.config import SENSORS
from gate_control.__classes__.Sensor import Sense
from gate_control.__classes__.Events import event

from datetime import datetime as dt
from time import sleep
import argparse


Button = Sense(gpio=SENSORS['GPIO']['BT'],id='momentary switch')
ts = lambda:dt.now().timestamp()


def epoch(
         state:int=0
        ,mock:bool=False
):
    return {
         'state':state
        ,'mock':mock
    }

def eval_history(hist:dict)->dict:
    '''
    params:
        hist:dict - The dictionary containing the historical data for the button sense iterator.
    Takes the historical data and evaluates what actions if any should occur as a result of the event history and outputs a truncated version of the history.

    returns:
        hist:dict
    '''
    assert(type(hist) is dict)
    keys = list(hist.keys())
    keys.sort()
    keys = keys[-30:]
    current_activations = [x for x in keys if x >= ts() - 1]
    prev_activations = [k for k,v in hist.items() if v.get('state') and k not in current_activations]
    action_space = {
          'ebrake':len(current_activations+prev_activations) == 30
        , 'activation':not(len(current_activations+prev_activations)) and current_activations
    }
    action = [k for k,v in action_space.items() if v]
    if action:
        action = action.pop()
    if not any([x for x in hist.values()['mock']]):
        event(action=action)
    else:
        print(f'mock {action}')
    return {k:v for k,v in hist.items() if k in keys}


def button_control_flow(mock=False):
    '''
    Check the state of the momentary switch at a defined cadence.
    If activated, sends message to the doorman and waits for feedback.
    '''
    hist = {}
    while True:
        if Button.get_state():
            hist.update({ts():epoch(state=1,mock=mock)})
        else:
            hist.update({ts():epoch(state=0,mock=mock)})
        hist = eval_history(hist)
        sleep(SENSORS['PING'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mock", type=int, help = "Mock Status")
    args = parser.parse_args()
    button_control_flow(mock=args.mock)