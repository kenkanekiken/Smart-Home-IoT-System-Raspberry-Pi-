import RPi.GPIO as G

FAN_PIN = 17

def turn_on_fan(temp):
    if temp > 32:
        G.output(FAN_PIN, 1)
    else:
        G.output(FAN_PIN, 0)
    