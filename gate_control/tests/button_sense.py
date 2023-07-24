from gate_control.button_sense import *

def epoch_test():
    print('testing','epoch_test')
    t1 = epoch()
    t2 = epoch(state=1)
    t3 = epoch(mock=1)
    assert(t1['state']==0 and t1['mock'] == False)
    assert(t2['state']==1 and t2['mock'] == False)
    assert(t3['state']==0 and t3['mock'] == True)
    print('passed')
    return 1


def filter_history_test():
    print('testing','filter_history_test')
    hist = {}
    for x in range(45):
        hist.update({ts():epoch()})
        sleep(SENSORS['PING'])
    current = filter_history(hist,'current')
    previous = filter_history(hist,'previous')
    last_30 = filter_history(hist,'last_30')

    assert(len(last_30)<=30)
    assert(all([ts()-x <= 1 for x in current]))
    assert(all([not(ts()-x <= 1) for x in previous]))
    return 1

def get_current_activations_test():
    print('testing','get_current_activations_test')
    hist = {}
    for x in range(45):
        hist.update({ts():epoch(state=1)})
        sleep(SENSORS['PING'])
    assert(any(get_current_activations(hist)))

    hist = {}
    for x in range(45):
        hist.update({ts():epoch(state=0)})
        sleep(SENSORS['PING'])
    
    assert(len(get_current_activations(hist))==0)
    print('passed')
    return 1

def get_all_activations_test():
    print('testing','get_all_activations_test')
    hist = {}
    for x in range(45):
        hist.update({ts():epoch(state=1)})
        sleep(SENSORS['PING'])
    assert(len(get_all_activations(hist))==30)

    hist = {}
    for x in range(45):
        hist.update({ts():epoch(state=0)})
        sleep(SENSORS['PING'])
    
    assert(len(get_all_activations(hist))==0)
    print('passed')
    return 1

def action_triage_test():
    print('testing','action_triage_test')
    hist = {}
    for x in range(45):
        hist.update({ts():epoch()})
        sleep(SENSORS['PING'])
    current = get_current_activations(hist)
    last_30 = get_all_activations(hist)
    assert(action_triage(current=current,last_30=last_30) == None)

    hist = {}
    for x in range(45):
        hist.update({ts():epoch(state=1)})
        sleep(SENSORS['PING'])
    current = get_current_activations(hist)
    last_30 = get_all_activations(hist)
    assert(action_triage(current=current,last_30=last_30) == 'ebrake')

    hist = {}
    for x in range(30):
        hist.update({ts():epoch()})
        sleep(SENSORS['PING'])
    sleep(2)
    for x in range(5):
        hist.update({ts():epoch(state=1)})
        sleep(SENSORS['PING'])
    current = get_current_activations(hist)
    last_30 = get_all_activations(hist)
    assert(action_triage(current=current,last_30=last_30) == 'activation')
    
    print('passed')
    return 1



def run_all_tests():
    assert(epoch_test()==1)
    assert(filter_history_test()==1)
    assert(get_current_activations_test()==1)
    assert(get_all_activations_test()==1)
    assert(action_triage_test()==1)


if __name__ == '__main__':
    run_all_tests()