from gate_control import GPIO

class Relay:

    def __init__(self,gpio) -> None:
        self.gpio = gpio
        GPIO.setup(self.gpio['ON'], GPIO.OUT)
        GPIO.setup(self.gpio['OFF'], GPIO.OUT)

    def get_state(self):
        state = f'test {self.gpio}'
        return state
    
    def close(self):
        GPIO.output(self.gpio['OFF'], 0)
        GPIO.output(self.gpio['ON'], 1) # is this pin on all the time?

    def open(self):
        GPIO.output(self.gpio['ON'], 0) 
        GPIO.output(self.gpio['OFF'], 1) # is this pin on all the time?