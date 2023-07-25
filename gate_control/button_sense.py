# This mock system is over-engineered and should be simplified.
# There is no reason to include and evaluate is as the historical dict.
# This means that the history eval should be modified to a list.
# Which makes some of the filtering methods unnecessary.

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

def filter_history(hist:dict,method:str):
    keys = sorted(list(hist.keys()))
    t = ts()
    return {
         'current':lambda:{k:v for k,v in hist.items() if (t-k) <= 1}
        ,'previous':lambda:{k:v for k,v in hist.items() if (t-k) > 1}
        ,'last_30':lambda:{k:v for k,v in hist.items() if k in keys[-30:]}
    }[method]()

def get_activations(hist:dict):
    return [k for k,v in hist.items() if v['state'] == 1]

def get_current_activations(hist:dict):
    current = filter_history(hist,'current')
    return get_activations(current)

def get_prev_activations(hist:dict):
    previous = filter_history(hist,'previous')
    return get_activations(previous)

def get_all_activations(hist:dict):
    last_30 = filter_history(hist,'last_30')
    return get_activations(last_30)

def action_triage(current:list,last_30:list):
    actions = {
          'ebrake':len(last_30) == 30
        , 'activation':not(len(last_30) == 30) and current
    }
    action_determination = [k for k,v in actions.items() if v]
    assert(len(action_determination) <= 1)
    if action_determination:
        return action_determination.pop()

def eval_history(hist:dict)->dict:
    '''
    params:
        hist:dict - The dictionary containing the historical data for the button sense iterator.
    Takes the historical data and evaluates what actions if any should occur as a result of the event history and outputs a truncated version of the history.

    returns:
        hist:dict
    '''

    action = action_triage(
         current=get_current_activations(hist)
        ,last_30=get_all_activations(hist)
    )
    if action:
        if not any([x['mock'] for x in hist.values()]):
            event(action=action)
        else:
            print(f'mock {action}')
    return filter_history(hist,'last_30')


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