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


DOOR_TRAVEL_TIME = 10
START_STATE = 'DN' # UP DN NA
METHOD = 'TIME'