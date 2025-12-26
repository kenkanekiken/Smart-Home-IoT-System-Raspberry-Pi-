import RPi.GPIO as G
import time

def led_green():
    G.output(16,1)
    time.sleep(1)
    G.output(16,0)
def led_red():
    G.output(20,1)
    time.sleep(1)
    G.output(20,0)