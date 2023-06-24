cd /home/gate/gate-controller
nohup python3 -m gate_control.doorman -m 0
nohup python3 -m gunicorn -w 4 -b 0.0.0.0 'gate_control.gate_api:app'
nohup python3 -m gate_control.button_sense -m 0