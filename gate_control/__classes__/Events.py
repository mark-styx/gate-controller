from datetime import datetime as dt
from gate_control.config import STREAM,CONSUMED
from gate_control import REVERE

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
        self.__add_event()
    
    def __add_event(self):
        self.id = REVERE.xadd(
             name=STREAM
            ,maxlen=100
            ,fields={
                 'action':self.action
                ,'ttl':self.ttl
                ,'doa':self.ttl + self.t
                ,'t':self.t
                ,'tstr':self.tstr
            }
        )
        self.await_claim()
    
    
    def await_claim(self):
        while True:
            if self.id in REVERE.lrange(name=CONSUMED,start=-5,end=-1):
                REVERE.ltrim(CONSUMED,-150,-1)
                return