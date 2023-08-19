# This mock system is over-engineered and should be simplified.
# There is no reason to include and evaluate is as the historical dict.
# This means that the history eval should be modified to a list.
# Which makes some of the filtering methods unnecessary.

from gate_control.config import SENSORS,SWITCH_EBRAKE,SWITCH_THRESHOLD
from gate_control.__classes__.Sensor import Sense
from gate_control.__classes__.Events import event
from gate_control import GPIO,log

from datetime import datetime as dt
from time import sleep
import argparse


Button = Sense(gpio=SENSORS['GPIO']['BT'],id='momentary switch',active=0)
ts = lambda:dt.now().timestamp()


def command_sequence(start):
    log('button_sense',3,'command sequence enter')
    while Button.get_state():
        sleep(SENSORS['PING'])
    end = ts()
    log('button_sense',3,f'button hold duration {end-start}')
    if (end - start) >= SWITCH_EBRAKE:
        log('button_sense',3,'ebrake resolved')
        return 'ebrake'
    elif (end-start) >= SWITCH_THRESHOLD:
        log('button_sense',3,'activation resolved')
        return 'activate'
    else:
        log('button_sense',3,'suspected false positive: press did not meet threshold!')

def button_control_flow(mock=False):
    log('button_sense',3,'button control flow enter')
    while True:
        if Button.get_state():
            log('button_sense',3,'button sensed')
            action = command_sequence(ts())
            print(action)
            event(action,source='button',MOCK=mock)
        sleep(SENSORS['PING'])



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mock", type=int, help = "Mock Status")
    args = parser.parse_args()
    try:
        button_control_flow(mock=args.mock)
    finally:
        GPIO.cleanup()
