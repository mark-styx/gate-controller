from flask import Flask,request
from gate_control.config import RELAYS,SENSORS
from gate_control.control import Gate

HelmsDeep = Gate(RELAYS=RELAYS,SENSORS=SENSORS)

app = Flask(__name__)
@app.route('/gate', methods=['get','post'])
def gate_trigger():
   if request.method.lower() == 'post':
      HelmsDeep.activate()
      return 'triggered'
   if request.method.lower() == 'get':
      return HelmsDeep.get_door_state()


if __name__ == '__main__':
    app.run(port=8081)