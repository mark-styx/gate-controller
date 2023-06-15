from gate_control.control import *
from gate_control import REVERE

from flask import Flask,request
from datetime import datetime as dt

app = Flask(__name__)
@app.route('/gate/open', methods=['post'])
def gate_open():
   if request.data.get('mock'):
      return 'Mock Open Request'
   REVERE.mset({"task":"UP","t":dt.now().timestamp()})
   return 'opening'

@app.route('/gate/close', methods=['post'])
def gate_close():
   if request.data.get('mock'):
      return 'Mock Close Request'
   REVERE.mset({"task":"DN","t":dt.now().timestamp()})
   return 'closing'

@app.route('/gate/status', methods=['get'])
def gate_status():
   if request.data.get('mock'):
      return 'Mock Status Request'
   return REVERE.get("state")


if __name__ == '__main__':
    app.run(port=8081)