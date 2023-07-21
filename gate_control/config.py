RELAYS = {
    "GPIO":{
          "UP":{"ON":22,"OFF":29}
        , "DN":{"ON":36,"OFF":31}
    }
}

SENSORS = {
    "GPIO":{
        "BT":21
        #,"UP":0
        #, "DN":0
    },
    "PING":.8
}


STREAM='HELMS_DEEP'
DOOR_TRAVEL_TIME = 12
START_STATE = 'DN' # UP DN NA
CADENCE = .05

PULSE = .5
PULSE_DELAY = .25
