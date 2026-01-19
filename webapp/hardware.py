import time

try:
    import RPi.GPIO as GPIO
    ON_PI = True
except Exception:
    GPIO = None
    ON_PI = False

# ---- Pin mapping ----
PIN_RELAY_FAN = 17      # Relay for fan
PIN_BUZZER = 21         # Buzzer

PIN_SERVO_DOOR = 13     # Door servo
PIN_SERVO_WINDOW = 12   # Window servo
PIN_SERVO_LAUNDRY = 19  # Laundry servo

# ---- Memory status ----
_status = {
    "door": "closed",
    "window": "closed",
    "laundry": "retracted",
    "fan": "off",
    "buzzer": "off",
    "on_pi": ON_PI,
}

# ---- Global variable ----
override = False
# ---- Servo PWM objects ----
_pwm_door = None
_pwm_window = None
_pwm_laundry = None

def init():
    """Initialize GPIO + PWM."""
    global _pwm_door, _pwm_window, _pwm_laundry

    if not ON_PI:
        print("[hardware] Not on Raspberry Pi. Running in MOCK mode.")
        return

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Outputs
    GPIO.setup(PIN_RELAY_FAN, GPIO.OUT)
    GPIO.setup(PIN_BUZZER, GPIO.OUT)

    GPIO.setup(PIN_SERVO_DOOR, GPIO.OUT)
    GPIO.setup(PIN_SERVO_WINDOW, GPIO.OUT)
    GPIO.setup(PIN_SERVO_LAUNDRY, GPIO.OUT)

    # Default off
    GPIO.output(PIN_RELAY_FAN, GPIO.LOW)
    GPIO.output(PIN_BUZZER, GPIO.LOW)

    # Servos at 50Hz
    _pwm_door = GPIO.PWM(PIN_SERVO_DOOR, 50)
    _pwm_window = GPIO.PWM(PIN_SERVO_WINDOW, 50)
    _pwm_laundry = GPIO.PWM(PIN_SERVO_LAUNDRY, 50)

    _pwm_door.start(0)
    _pwm_window.start(0)
    _pwm_laundry.start(0)

def cleanup():
    if ON_PI:
        GPIO.cleanup()

def get_status():
    return dict(_status)

def _set_servo_angle(pwm, angle: int):
    if not ON_PI:
        return

    duty = 2 + (angle / 18.0)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.35)
    pwm.ChangeDutyCycle(0)

def door_open():
    global _status
    _set_servo_angle(_pwm_door, 180)
    _status["door"] = "open"
    return True, "Door opened"

def door_close():
    global _status
    _set_servo_angle(_pwm_door, 90)
    _status["door"] = "closed"
    return True, "Door closed"

def window_open():
    global _status
    _set_servo_angle(_pwm_window, 90)
    _status["window"] = "open"
    return True, "Window opened"

def window_close():
    global _status
    _set_servo_angle(_pwm_window, 0)
    _status["window"] = "closed"
    return True, "Window closed"

def laundry_extend():
    global _status
    _set_servo_angle(_pwm_laundry, 90)
    _status["laundry"] = "extended"
    return True, "Laundry extended"

def laundry_retract():
    global _status
    _set_servo_angle(_pwm_laundry, 180)
    _status["laundry"] = "retracted"
    return True, "Laundry retracted"

def fan_on():
    global _status, override
    override = True
    if ON_PI:
        GPIO.output(PIN_RELAY_FAN, GPIO.HIGH)
    _status["fan"] = "on"
    return True, "Fan ON"

def fan_off():
    global _status, override
    override = False
    if ON_PI:
        GPIO.output(PIN_RELAY_FAN, GPIO.LOW)
    _status["fan"] = "off"
    return True, "Fan OFF"

def buzzer_beep():
    global _status
    _status["buzzer"] = "beep"
    if ON_PI:
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(0.15)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
    _status["buzzer"] = "off"
    return True, "Buzzer beeped"

def perform_action(device: str, action: str):
    routes = {
        ("door", "open"): door_open,
        ("door", "close"): door_close,
        ("window", "open"): window_open,
        ("window", "close"): window_close,
        ("laundry", "extend"): laundry_extend,
        ("laundry", "retract"): laundry_retract,
        ("fan", "on"): fan_on,
        ("fan", "off"): fan_off,
        ("buzzer", "beep"): buzzer_beep,
    }

    fn = routes.get((device, action))
    if not fn:
        return False, f"Unknown action: {device}.{action}"
    return fn()
