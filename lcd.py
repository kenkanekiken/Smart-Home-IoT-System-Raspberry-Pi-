from rpi_lcd import LCD
import time

lcd = LCD()

def lcdReading(temp, hum):
#     lcd.text(f"Temp: {temp:.2f}", 1)
#     lcd.text(f"Hum: {hum:.2f}", 2)
    safe_text(f"Temp: {temp:.2f}", 1)
    safe_text(f"Hum: {hum:.2f}", 2)

def safe_text(msg, line):
    try:
        lcd.text(str(msg)[:16], line)   # trim to 16 chars
    except OSError as e:
        print("LCD I2C error:", e)
        # optional small cooldown so bus can recover
        time.sleep(0.05)

def clear_safe():
    try:
        lcd.clear()
    except OSError as e:
        print("LCD clear error:", e)

