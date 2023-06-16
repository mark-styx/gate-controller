from gate_control import GPIO

class Sense:

    def __init__(self,gpio,id,active=0) -> None:
        self.id = id
        self.gpio = gpio
        self.active = active
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_state(self)->bool:
        state = GPIO.input(self.gpio)
        if state == self.active:
            print(f'sensed {self.id}')
        return state == self.active