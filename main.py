import RPi.GPIO as G 
import bme_sensor, fan, lcd
import time

G.setwarnings(False)
G.setmode(G.BCM)
G.setup(17,G.OUT)

last_sensor = 0
last_lcd = 0
try:
#     bme_sensor.bmeRead() #Temperature reading every 2 second
#     lcd.lcd_reading() #LCD display Temp/Hum reading every 2 second
    while True:
        now = time.time()
        
        #Temperature reading every 2 second
        if (now - last_sensor >= 2):
            bme_sensor.bmeRead() 
            last_sensor = now
            
        #LCD display Temp/Hum reading every 2 second
        if (now - last_lcd >= 2):
            lcd.lcd_reading(bme_sensor.data.temperature, bme_sensor.data.humidity)
            last_lcd = now
            
            
        fan.turn_on_fan(bme_sensor.data.temperature) #Turn on/off the fan
        time.sleep(0.1)
        
except KeyboardInterrupt:
    pass
finally:
    G.cleanup()
        