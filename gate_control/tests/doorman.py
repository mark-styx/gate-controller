from gate_control.doorman import *
from gate_control.__classes__.Events import event

gate = pigate(MOCK=True)


def interrupt_test():
    print('interrupt test')
    assert(gate.interrupt()=='Interrupted')
    print('passed\n\n')
    return 1

def activate_test():
    print('activate test')
    assert(gate.activate(gate.UP)==f'{gate.UP.id} Activate')
    print('passed\n\n')
    return 1

def toggle_ebrake_test():
    print('ebrake test')
    start = gate.ebrake_active
    gate.toggle_ebrake()
    end = gate
    assert(start != end)
    print('passed\n\n')
    return 1

def toggle_ebrake_test2():
    print('ebrake test2')
    if not gate.ebrake_active:
        gate.toggle_ebrake()
    assert(gate.activate(gate.UP) == 'Ebrake is Active, No Actions May Be Taken')
    print('passed\n\n')
    return 1

def activation_flow_test():
    print('activation_flow_test')
    gate = pigate(MOCK=True)
    event = gate.activation_flow()
    print(event)
    assert(event['target']=='UP')
    assert(event['completion_time'] - gate.UP.t >= DOOR_TRAVEL_TIME)
    print('passed\n\n')
    return 1

def action_triage_test():
    print('action_triage_test')
    gate = pigate(MOCK=True)
    event1 = gate.action_triage('activate')
    event2 = gate.action_triage('ebrake')
    assert(event1 == 'activate')
    assert(event2 == 'ebrake')
    print('passed\n\n')
    return 1

def get_active_relay_test():
    print('get_active_relay_test')
    gate = pigate(MOCK=True)
    gate.activate(gate.UP)
    assert(gate.get_active_relay() is gate.UP)
    print('passed\n\n')
    return 1

def get_door_motion_test():
    print('get_door_motion_test')
    gate = pigate(MOCK=True)
    gate.activate(gate.UP)
    gate.get_door_motion()
    assert(gate.door_state == 'Opening')
    print('passed\n\n')
    return 1

def stream_event_test():
    print('stream_event_test')
    gate = pigate(MOCK=True)
    event('activate',MOCK=True)
    E = gate.stream_event()
    print(E)
    assert(E['target']=='UP')
    print('passed\n\n')
    return 1

if __name__ == '__main__':
    interrupt_test()
    activate_test()
    toggle_ebrake_test()
    toggle_ebrake_test2()
    activation_flow_test()
    action_triage_test()
    get_active_relay_test()
    get_door_motion_test()
    stream_event_test()