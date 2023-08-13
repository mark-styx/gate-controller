from gate_control import REVERE
from gate_control.config import STREAM,CONSUMED

consumed = REVERE.lrange(CONSUMED,0,REVERE.llen(CONSUMED))
events = REVERE.xread(streams={STREAM:0})
events = events[0][1]
keys = [k[0] for k in events]
new_events = [x for x in keys if x not in consumed]

print('events:',events)
print('new events:',new_events)
print('consumed:',consumed)
