from gate_control import REVERE
from gate_control.config import CADENCE

from flask import Flask,request
from datetime import datetime as dt
from time import sleep

ts = lambda:dt.now().timestamp()

def __opposite_direction__(current_state):
   travel = {
         'UP':'DN'
      , 'DN':'UP'
      , 'NA':'DN'
   }
   target = travel.get(current_state)
   if not target:
      target = REVERE.get('task')
   return target


app = Flask(__name__)
@app.route('/gate/activate', methods=['post'])
def gate_activate():
   t = ts()
   if request.json.get('mock'):
      msg = 'Mock Activate Request'
      print(msg)
      return msg
   cstate,ct = REVERE.mget(["state","t"])
   if t - float(ct) < 1:
      msg = 'Not enough time between requests, ignoring'
      print(msg)
      return msg
   task = __opposite_direction__(cstate)
   REVERE.mset({"task":task,"t":ts()})
   while cstate not in ['Opening','Closing']:
      cstate = REVERE.get("state")
      sleep(CADENCE)
   return cstate

@app.route('/gate/status', methods=['get'])
def gate_status():
   if request.json.get('mock'):
      msg = 'Mock Status Request'
      print(msg)
      return msg
   return REVERE.get("state")


if __name__ == '__main__':
    app.run(port=8081)