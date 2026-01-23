import RPi.GPIO as G
import time
import lcd
import buzzer

pwm_door = None
pwm_window = None
pwm_laundry = None
doorOpen = False
doorOpen_time = 0.0
open_request = False
last_state = None

door_status = None

def pwmInit():
    global pwm_door, pwm_window, pwm_laundry
    pwm_door = G.PWM(13,50)
    pwm_door.start(0)
    
    pwm_window = G.PWM(19,50) 
    pwm_window.start(0)
    
    pwm_laundry = G.PWM(12,50) 
    pwm_laundry.start(0)
    
    time.sleep(0.2)

    set_angle_door(90)
    set_angle_window(90)
    set_angle_laundry(90)
    

def pwmStop():
    global pwm_door, pwm_window, pwm_laundry
    if pwm_door is not None:
        pwm_door.stop()
        pwm_door = None
    if pwm_window is not None:
        pwm_window.stop()
        pwm_window = None
    if pwm_laundry is not None:
        pwm_laundry.stop()
        pwm_laundry = None
    
def set_angle_door(angle):
    duty = 2 + (angle / 18)
    pwm_door.ChangeDutyCycle(duty)
    time.sleep(0.3)
    pwm_door.ChangeDutyCycle(0)

def doorStatus():
    if open_request:
        door_status = "Open"
    else:
        door_status = "Close"
    return door_status

def trigger_open():
    global open_request
    open_request = True

def door_open():
    global doorOpen, doorOpen_time, open_request
    now = time.time()
    # --- Open on request (only once) ---
    if open_request and not doorOpen:
        set_angle_door(180)
        doorStatus = "Open"
        print("Door Open for 3 Second")
        lcd.clear_safe()
        lcd.safe_text("Door Open",1)
        time.sleep(1)
        doorOpen = True
        doorOpen_time = now
        open_request = False   # consume the request

    # --- Close after 3 seconds ---
    if doorOpen and (now - doorOpen_time >= 3):
        set_angle_door(90)
        doorStatus = "Close"
        print("Door Close")
        doorOpen = False

def set_angle_laundry(angle):
    duty = 2 + (angle / 18)
    pwm_laundry.ChangeDutyCycle(duty)
    time.sleep(0.3)
    pwm_laundry.ChangeDutyCycle(0)

def set_angle_window(angle):
    duty = 2 + (angle / 18)
    pwm_window.ChangeDutyCycle(duty)
    time.sleep(0.3)
    pwm_window.ChangeDutyCycle(0)
    
def window_open(rain_value):
    global last_state
    is_raining = rain_value < 500

    if is_raining != last_state:
        if is_raining:
            print("🌧️ Rain detected")
            set_angle_window(180)
            print("Window Close")
            set_angle_laundry(0)
            print("Laundry Pole Retract")
            lcd.clear_safe()
            lcd.safe_text("Window Close",1)
            lcd.safe_text("Pole Retract",2)
        else:
            print("☀️ Sunny")
            set_angle_window(90)
            print("Window Open")
            set_angle_laundry(90)
            print("Laundry Pole Extend")
            lcd.safe_text("Window Open",1)
            lcd.safe_text("Pole Extend",2)
        last_state = is_raining
        