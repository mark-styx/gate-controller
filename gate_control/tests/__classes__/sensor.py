from gate_control.button_sense import Sense


def state_test():
    sensor1 = Sense(1,'UP')
    assert(sensor1.get_state() == 1)


if __name__ == '__main__':
    state_test()