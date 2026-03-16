try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    MOCK_MODE = False
except:
    from gate_control.__classes__.MockPins import MockGPIO
    GPIO = MockGPIO()
    MOCK_MODE = True

import redis
import time

def get_redis_connection(max_retries=5, retry_delay=2):
    """Get Redis connection with retry logic"""
    for attempt in range(max_retries):
        try:
            client = redis.Redis(decode_responses=True)
            client.ping()  # Test connection
            return client
        except redis.ConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Redis connection failed (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect to Redis after {max_retries} attempts")
                raise

REVERE = get_redis_connection()

from gate_control.__classes__.Logging import log
