import RPi.GPIO as G
import time
import lcd

pwm_door = None
pwm_window = None
pwm_laundry = None
doorOpen = False
doorOpen_time = 0.0
open_request = False
last_state = None

def pwmInit():
    global pwm_door
    pwm_door = G.PWM(13,50)
    pwm_door.start(90)
    
    global pwm_window
    pwm_window = G.PWM(19,50)
    pwm_window.start(90)
    
    global pwm_laundry
    pwm_laundry = G.PWM(12,50)
    pwm_laundry.start(90)

def pwmStop():
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

def trigger_open():
    global open_request
    open_request = True

def door_open():
    global doorOpen, doorOpen_time, open_request
    now = time.time()
    # --- Open on request (only once) ---
    if open_request and not doorOpen:
        set_angle_door(180)
        print("Door Open for 3 Second")
        lcd.lcd.text("Door Open",1)
        lcd.lcd.text("for 3 second",2)
        time.sleep(1)
        doorOpen = True
        doorOpen_time = now
        open_request = False   # consume the request

    # --- Close after 3 seconds ---
    if doorOpen and (now - doorOpen_time >= 3):
        set_angle_door(90)
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
            set_angle_window(180) # e laundry
            print("Window Close")
            set_angle_laundry(0) # e window
            print("Laundry Pole Retract")
            lcd.lcd.text("Window Close",1)
            lcd.lcd.text("Pole Retract",2)
        else:
            print("☀️ Sunny")
            set_angle_window(90) #this is now laundry pole
            print("Window Open")
            set_angle_laundry(90) #this is now window 
            print("Laundry Pole Extend")
            lcd.lcd.text("Window Open",1)
            lcd.lcd.text("Pole Extend",2)
        last_state = is_raining
        