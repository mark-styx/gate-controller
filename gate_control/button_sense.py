from gate_control import GPIO
from gate_control.config import SENSORS,HOST
from gate_control.__classes__.Sensor import Sense

from datetime import datetime as dt
from time import sleep
import requests,argparse


Button = Sense(gpio=SENSORS['GPIO']['BT'],id='momentary switch')
tchk = lambda: dt.now().timestamp()

def send_gate_signal(mock):
    resp = requests.post(f'http://{HOST}/gate/activate'
                         , headers={'content-type':'application/json'}
                         , data={'mock':mock})
    print(resp.status_code,resp.content)
    return resp

def button_control_flow(mock=False):
    '''
    check the state of the momentary switch at a defined cadence
    if activated, send data to api to trigger the gate
    '''

    t = dt.now().timestamp()
    while True:
        if Button.get_state() and (tchk() - t >= 1):
            send_gate_signal(mock)
            t = tchk()
        sleep(SENSORS['PING'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mock", type=int, help = "Mock Status")
    args = parser.parse_args()
    button_control_flow(mock=args.mock)