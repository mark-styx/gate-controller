from gate_control import GPIO

class Sense:

    def __init__(self,gpio,id) -> None:
        self.id = id
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_state(self)->bool:
        state = GPIO.input(self.gpio)
        if state:
            print(f'sensed {self.id}')
        return state