from datetime import datetime as dt
from pathlib import Path

from gate_control.config import LOG_LEVEL

folder = Path().home()

def log(path,log_level,details):
    if LOG_LEVEL > log_level: return
    if not folder.exists():
        folder.mkdir()
    with open(folder/f'{path}.txt','a') as f:
        f.write(str(details) + '\n')