import RPi.GPIO as GPIO
import redis

REVERE = redis.Redis(decode_responses=True)
GPIO.setmode(GPIO.BOARD)