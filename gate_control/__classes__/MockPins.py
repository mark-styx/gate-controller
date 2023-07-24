class MockGPIO:

    def __init__(self) -> None:
        self.state = 0

    
    def OUT(self):
        pass

    def output(self,pin,state):
        self.state = state

    def input(self,pin):
        return self.state

    def IN(self):
        pass

    def PUD_UP(self):
        pass

    def setup(self,pin,pinType,pull_up_down=None):
        self.pin = pin
        self.pintType = pinType

    def get_state(self):
        return self.state
