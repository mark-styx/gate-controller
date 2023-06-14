from gate_control.__classes__.Switch import Relay,sleep

r = Relay({'ON':22,'OFF':29})
r.open()