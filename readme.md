

Door Logic
Sensors
    - Close Sensor
    - Open Sensor
    - Blocked Sensor
    - Momentary Switch
Switches
    - Up Relay
    - Down Relay




Event Handler
Event Creators - Switches, Sensors, API


Gate
    - Sensor
        - State
        - prevState
    - Switch
        - State
        - prevState
    - State
        - History
        - Log
        - Status

probably go back to the handler idea; 
the current issue is having a useful event queue
that can handle interuptions


handler - read and react to events msg api when done
api - create events
|_ sensors - message api