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
      , 'Opening':'DN'
      , 'Closing':'UP'
   }
   return travel.get(current_state)


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
   if task:
      REVERE.mset({"task":task,"t":ts()})
   else:
      return 'Error: Improper Target'
   while cstate not in ['Opening','Closing']:
      cstate = REVERE.get("state")
      sleep(CADENCE)
   return cstate

@app.route('/gate/status', methods=['post'])
def gate_status():
   if request.json.get('mock'):
      msg = 'Mock Status Request'
      print(msg)
      return msg
   return REVERE.get("state")

@app.route('/gate/ebrake', methods=['post','get'])
def gate_ebrake():
   if request.json.get('mock'):
      msg = 'Mock Status Request'
      print(msg)
      return msg
   ebrake = REVERE.get('ebrake')
   if request.method.lower() == 'get':
      return f'ebrake: {ebrake}'
   elif request.method.lower() == 'post':
      new = {'ON':'OFF','OFF':'ON'}[ebrake]
      REVERE.mset({'ebrake':new,'ebrake_eid':ts()})
      return f'setting ebrake: {new}'


if __name__ == '__main__':
    app.run(port=8081)