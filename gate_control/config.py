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
    "PING":.125
}


DOOR_TRAVEL_TIME = 13
START_STATE = 'DN' # UP DN NA
METHOD = 'TIME'
HOST = '192.168.1.83:8000'
CADENCE = .125

PULSE = 1
PULSE_DELAY = .5