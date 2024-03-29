from gate_control import REVERE
from gate_control.__classes__.Events import event

from flask import Flask,request
from datetime import datetime as dt
from time import sleep

ts = lambda:dt.now().timestamp()

app = Flask(__name__)

@app.route('/gate/activate', methods=['post'])
def gate_activate():
   if request.json.get('mock'):
      msg = 'Mock Activate Request'
      print(msg)
      return msg
   event('activate',source='api')
   sleep(1.5)
   return REVERE.get("state")

@app.route('/gate/status', methods=['get'])
def gate_status():
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
      event('ebrake',source='api')
      return f'toggling ebrake'


if __name__ == '__main__':
    app.run(port=8081)