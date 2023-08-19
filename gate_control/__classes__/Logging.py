from gate_control.config import LOGS,LOG_STATE

from datetime import datetime as dt
from pathlib import Path

def logger(func):
    def execute(*args,**kwargs):
        if LOG_STATE:
            log(func.__name__,str({
                't':dt.now().timestamp()
                ,'tstr':str(dt.now())
                ,'args':f'{args}'
                ,'kwargs':f'{kwargs}'
            }))
        func(*args,**kwargs)
    return execute

def log(path,details):
    folder = Path.home() / LOGS
    if not folder.exists():
        folder.mkdir()
    with open(folder/f'{path}.txt','a') as f:
        f.write(details)
