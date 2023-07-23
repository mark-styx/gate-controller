from gate_control import REVERE
from gate_control.config import DOOR_TRAVEL_TIME
from gate_control.__classes__.Events import event

from flask import Flask,request
from datetime import datetime as dt
from time import sleep

ts = lambda:dt.now().timestamp()

app = Flask(__name__)
last = 0

'''
keep list of ts's and then compare the last two to see if a partial 
execution is required.
'''

@app.route('/gate/activate', methods=['post'])
def gate_activate():
   if request.json.get('mock'):
      msg = 'Mock Activate Request'
      print(msg)
      return msg
   if ts() - last < 1:
      return 'Activation Requested too early'
   last = ts()
   event('activate')
   return REVERE.get("state")

@app.route('/gate/status', methods=['post'])
def gate_status():
   if request.json.get('mock'):
      msg = 'Mock Status Request'
      print(msg)
      return msg
   return REVERE.get("state")

@app.route('/gate/ebrake', methods=['post','get'])
def gate_ebrake():
   ebrake = REVERE.get('ebrake')
   if request.method.lower() == 'get':
      return f'ebrake: {ebrake}'
   elif request.method.lower() == 'post':
      if request.json.get('mock'):
         msg = 'Mock ebrake Request'
         print(msg)
         return msg
      event('ebrake')
      return f'toggling ebrake'


if __name__ == '__main__':
    app.run(port=8081)