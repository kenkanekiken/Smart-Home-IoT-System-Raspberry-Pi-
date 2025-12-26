import RPi.GPIO as G
G.setwarnings(False)
G.setmode(G.BCM)
print("GPIO mode set")

import bme_sensor, fan, lcd, rfid, servo, rainsensor, buzzer, led
import time
print("Import done")

G.setup(17,G.OUT) #Relay
#rfid servo 
G.setup(13,G.OUT) #Door
G.setup(19,G.OUT) #Window
G.setup(12,G.OUT) #Laundry
#buzzer
G.setup(21,G.OUT) #Buzzer
#led
G.setup(16,G.OUT) #LED Green
G.setup(20,G.OUT) #LED Red

last_sensor = 0
last_lcd = 0
last_rfid = 0
last_rain = 0

rain_value = 1023

try:
    rfid.start()
    servo.pwmInit()
    buzzer.buzzInit()
    while True:
        now = time.time()
        
        #Temperature reading every 2 second
        if (now - last_sensor >= 5):
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
                led.led_green()
                buzzer.buzz()
            else:
                led.led_red()
                buzzer.buzz_deny()
            rfid.latest_id = None   # clear so it doesn't repeat
        
        #Rain reading every 5 second
        if (now - last_rain >= 2):
            rain_value = rainsensor.read_adc(0)
            print("Rain ADC:", rain_value)
            last_rain = now
        
        fan.turn_on_fan(bme_sensor.data.temperature) #Turn on/off the fan
        servo.door_open()
        servo.window_open(rain_value)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    pass
finally:
    servo.pwmStop()
    spi.close()                                      
    G.cleanup()
        