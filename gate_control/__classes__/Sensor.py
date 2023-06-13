from gate_control import GPIO

class Sense:

    def __init__(self,gpio) -> None:
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_state(self):
        return GPIO.input(self.gpio)