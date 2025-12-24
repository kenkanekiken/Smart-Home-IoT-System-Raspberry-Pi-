import RPi.GPIO as G
G.setwarnings(False)
G.setmode(G.BCM)
print("GPIO mode set")

import bme_sensor, fan, lcd, rfid, servo 
import time
print("Import done")

G.setup(17,G.OUT)

#rfid servo 
G.setup(13,G.OUT) 

last_sensor = 0
last_lcd = 0
last_rfid = 0

try:
    rfid.start()
    servo.pwmInit()
    while True:
        now = time.time()
        
        #Temperature reading every 2 second
        if (now - last_sensor >= 2):
            bme_sensor.bmeRead() 
            last_sensor = now
            
        #LCD display Temp/Hum reading every 2 second
        if (now - last_lcd >= 2):
            lcd.lcdReading(bme_sensor.data.temperature, bme_sensor.data.humidity)
            last_lcd = now
        
        #RFID reading every 1 second
        if rfid.latest_id is not None:
            print("Card:", rfid.latest_id)
            if rfid.latest_id == 283513489777:
                servo.trigger_open()
            rfid.latest_id = None   # clear so it doesn't repeat
            
        fan.turn_on_fan(bme_sensor.data.temperature) #Turn on/off the fan
        servo.door_open()
        time.sleep(0.1)
        
except KeyboardInterrupt:
    pass
finally:
    servo.pwmStop()
    G.cleanup()
        