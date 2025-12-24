import RPi.GPIO as G
import time

pwm = None
doorOpen = False
doorOpen_time = 0.0
open_request = False

def pwmInit():
    global pwm
    pwm = G.PWM(13,50)
    pwm.start(0)

def pwmStop():
    global pwm
    if pwm is not None:
        pwm.stop()
        pwm = None
    
def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    pwm.ChangeDutyCycle(0)

def trigger_open():
    global open_request
    open_request = True

def door_open():
    global doorOpen, doorOpen_time, open_request
    now = time.time()

    # --- Open on request (only once) ---
    if open_request and not doorOpen:
        set_angle(180)
        print("angle 180")
        doorOpen = True
        doorOpen_time = now
        open_request = False   # consume the request

    # --- Close after 3 seconds ---
    if doorOpen and (now - doorOpen_time >= 3):
        set_angle(0)
        print("angle 0")
        doorOpen = False
        
        