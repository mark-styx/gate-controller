from datetime import datetime as dt

#from gate_control.config import STREAM
#from gate_control import REVERE

STREAM = 'gate-controller'
import redis

REVERE = redis.Redis(decode_responses=True)

class event:
    def __init__(
          self
        , action:str
        , ttl:int=0
    ) -> None:
        self.t = dt.now().timestamp()
        self.tstr = str(dt.now())
        self.action = action
        self.ttl = ttl
        self.id = None
    
    def add_event(self):
        self.id = REVERE.xadd(
             name=STREAM
            ,fields={
                 'action':self.action
                ,'ttl':self.ttl
                ,'doa':self.ttl + self.t
                ,'t':self.t
                ,'tstr':self.tstr
            }
        )
    
'''    def await_claim(self):
        REVERE.xread(streams=[STREAM].)'''