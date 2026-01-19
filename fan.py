import RPi.GPIO as G
import hardware
FAN_PIN = 17

def turn_on_fan(temp):
    if temp > 31 or hardware.override:
        print(hardware.override)
        G.output(FAN_PIN, 1)
    else:
        print(hardware.override)
        G.output(FAN_PIN, 0)
    