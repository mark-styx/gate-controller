from flask import Flask,request
from gate_control.control import *

HelmsDeep = Gate()

app = Flask(__name__)
@app.route('/gate/open', methods=['post'])
def gate_open():
   HelmsDeep.api_activate('UP')
   return 'opened'

@app.route('/gate/close', methods=['post'])
def gate_close():
   HelmsDeep.api_activate('DN')
   return 'closed'

if __name__ == '__main__':
    app.run(port=8081)