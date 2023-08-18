# This mock system is over-engineered and should be simplified.
# There is no reason to include and evaluate is as the historical dict.
# This means that the history eval should be modified to a list.
# Which makes some of the filtering methods unnecessary.

from gate_control.config import SENSORS,SWITCH_EBRAKE
from gate_control.__classes__.Sensor import Sense
from gate_control.__classes__.Events import event

from datetime import datetime as dt
from time import sleep
import argparse


Button = Sense(gpio=SENSORS['GPIO']['BT'],id='momentary switch',active=1)
ts = lambda:dt.now().timestamp()

def epoch(
         state:int=0
        ,mock:bool=False
):
    return {
         'state':state
        ,'mock':mock
        ,'triggered':False
    }

def filter_history(hist:dict,method:str):
    keys = sorted(list(hist.keys()))
    t = ts()
    return {
         'current':lambda:{k:v for k,v in hist.items() if (t-k) <= 1}
        ,'previous':lambda:{k for k,v in hist.items() if v['triggered'] and t-k <= 1}
        ,'last_30':lambda:{k:v for k,v in hist.items() if k in keys[-30:]}
    }[method]()

def get_activations(hist:dict):
    return [k for k,v in hist.items() if v['state'] == 1]

def get_current_activations(hist:dict):
    current = filter_history(hist,'current')
    return get_activations(current)

def get_prev_activations(hist:dict):
    previous = filter_history(hist,'previous')
    return len(previous) > 1

def get_all_activations(hist:dict):
    last_30 = filter_history(hist,'last_30')
    return get_activations(last_30)

def action_triage(current:list,last_30:list,prev:bool):
    actions = {
          'ebrake':len(last_30) == 30
        , 'activate':not(len(last_30) == 30) and current and not prev
    }
    action_determination = [k for k,v in actions.items() if v]
    assert(len(action_determination) <= 1)
    if action_determination:
        return action_determination.pop()

def _eval_history(hist:dict)->dict:
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
        ,prev=get_prev_activations(hist)
    )
    if action:
        if not any([x['mock'] for x in hist.values()]):
            event(action=action)
            hist[list(hist.keys())[-1]]['triggered']=True
        else:
            print(f'mock {action}')
    return filter_history(hist,'last_30')


def trunc_history(hist:dict)->dict:
    keys = sorted(list(hist.keys()))[-30:]
    hist = {k:v for k,v in hist.items() if k in keys}
    return hist
    
    
def eval_history(hist:dict,last_activation,mock)->dict:
    ebrake = all([v['state'] == 1 for v in hist.values()])
    if ebrake:
        event('ebrake',MOCK=mock)
    elif ts() - last_activation >= 1:
        event('activate',MOCK=mock)
    else:
        pass

# Instead of stream, consider batches of pulses
# Pulase Batch -> Evaluate -> Send
# Wait until command sequence has finished before sending
# Ex. If two pulses return True, then keep listening for the third one
# Pulse should return true if any of the checks return True during the pulse.

# Maybe Just check how long it was held?



def command_sequence(start):
    while Button.get_state():
        sleep(SENSORS['PING'])
    end = ts()
    if (end - start) >= SWITCH_EBRAKE:
        return 'ebrake'
    else:
        return 'activate'


def button_control_flow(mock=False):
    while True:
        if Button.get_state():
            action = command_sequence(ts())
            print(action)
            event(action,MOCK=mock)
        sleep(SENSORS['PING'])


def _button_control_flow(mock=False):
    '''
    Check the state of the momentary switch at a defined cadence.
    If activated, sends message to the doorman and waits for feedback.
    '''
    hist = {}
    last_activation = 0
    while True:
        if Button.get_state():
            print('sensed')
            hist.update({ts():epoch(state=1,mock=mock)})
            eval_history(hist,last_activation,mock)
            last_activation = ts()
        else:
            hist.update({ts():epoch(state=0,mock=mock)})
        hist = trunc_history(hist)
        sleep(SENSORS['PING'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mock", type=int, help = "Mock Status")
    args = parser.parse_args()
    button_control_flow(mock=args.mock)