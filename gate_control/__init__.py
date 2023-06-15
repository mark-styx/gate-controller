import RPi.GPIO as GPIO
import redis

REVERE = redis.Redis(decode_reponses=True)
GPIO.setmode(GPIO.BOARD)