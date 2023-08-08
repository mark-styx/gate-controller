RELAYS = {
    "GPIO":{
          "UP":{"ON":22,"OFF":29}
        , "DN":{"ON":36,"OFF":31}
    }
}

SENSORS = {
    "GPIO":{
        "BT":11
        #,"UP":0
        #, "DN":0
    },
    "PING":.1
}

ACTIONS = ['ebrake','activate']

STREAM='HELMS_DEEP'
CONSUMED = 'HD_Handled'
DOOR_TRAVEL_TIME = 10
START_STATE = 'DN' # UP DN NA
CADENCE = .05

PULSE = .5
PULSE_DELAY = .25
