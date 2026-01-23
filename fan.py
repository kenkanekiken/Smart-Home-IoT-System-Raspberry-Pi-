import RPi.GPIO as G
FAN_PIN = 17

fan_status = None

def turn_on_fan(temp):
    if temp > 28:
        G.output(FAN_PIN, 1)
    else:
        G.output(FAN_PIN, 0)
        
def fanStatus(temp):
    if temp > 28:
        fan_status = "On"
    else:
        fan_status = "Off"
    return fan_status
        
