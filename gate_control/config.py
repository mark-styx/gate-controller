RELAYS = {
    "GPIO":{
          "DN":{"ON":18,"OFF":12}
        , "UP":{"ON":33,"OFF":37}
    }
}

SENSORS = {
    "GPIO":{
        "BT":32
        #,"UP":0
        #, "DN":0
    },
    "PING":.1
}

ACTIONS = ['ebrake','activate']

STREAM='HELMS_DEEP'
CONSUMED = 'HD_Handled'
DOOR_TRAVEL_TIME = 9.15
START_STATE = 'DN' # UP DN NA
CADENCE = .05

SWITCH_EBRAKE = 1.5

PULSE = .5
PULSE_DELAY = .25
LOG_LEVEL = 0
