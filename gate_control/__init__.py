try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
except:
    from gate_control.__classes__.MockPins import MockGPIO
    GPIO = MockGPIO()

import redis
REVERE = redis.Redis(decode_responses=True)

from gate_control.__classes__.Logging import logger