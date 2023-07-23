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
    keys = list(hist.keys())
    keys.sort()
    keys = keys[-30:]
    current_activations = [x for x in keys if x >= ts() - 1]
    prev_activations = [x for x in hist if x.get('state') and x not in current_activations]
    action_space = {
          'ebrake':len(current_activations+prev_activations) == 30
        , 'partial_activation':prev_activations and current_activations and ((min(current_activations) - max(prev_activations)) >= 1)
        , 'activation':not(prev_activations) and current_activations
    }
    e = [k for k,v in action_space if v].pop()
    action = event(action=e)
    action.add_event()
    return {k:v for k,v in hist if k in keys}


def button_control_flow(mock=False):
    '''
    Check the state of the momentary switch at a defined cadence.
    If activated, sends message to the doorman and waits for feedback.
    '''
    hist = {}
    while True:
        if Button.get_state():
            hist[ts()] = epoch(state=1,mock=mock)
        else:
            hist[ts()] = epoch(mock=mock)
        hist = eval_history(hist)
        sleep(SENSORS['PING'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mock", type=int, help = "Mock Status")
    args = parser.parse_args()
    button_control_flow(mock=args.mock)