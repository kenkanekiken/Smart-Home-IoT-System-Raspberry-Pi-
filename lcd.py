from rpi_lcd import LCD

lcd = LCD()

def lcd_reading(temp, hum):
    lcd.text(f"Temp: {temp:.2f}", 1)
    lcd.text(f"Hum: {hum:.2f}", 2)
