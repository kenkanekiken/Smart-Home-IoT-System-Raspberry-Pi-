import RPi.GPIO as G
import time

#Buzzer using pwm
pwm_buzzer = None

def buzzInit():
    global pwm_buzzer
    pwm_buzzer = G.PWM(21, 1000)  # 1 kHz tone
    pwm_buzzer.stop()  # 50% duty cycle

def pwmStop():
    global pwm_buzzer
    if pwm_buzzer is not None:
        pwm_buzzer.stop()
        pwm_buzzer = None

def buzz():
    pwm_buzzer.start(50)
    time.sleep(0.3)
    pwm_buzzer.stop()
    
def buzz_deny():
    #Buzzer using pwm
    pwm_buzzer.start(50)
    pwm_buzzer.ChangeFrequency(1000)
    time.sleep(0.3)
    pwm_buzzer.ChangeFrequency(1500)
    time.sleep(0.3)
    pwm_buzzer.stop()