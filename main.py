import RPi.GPIO as G
G.setwarnings(False)
G.setmode(G.BCM)
print("GPIO mode set")
import os
import bme_sensor, fan, lcd, rfid, servo, rainsensor, buzzer, led
import time
import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
print("Import done")

token = "bntzzeAN8JahYHXWVgTSJLwouDuKgnjRSFPIo2Z0jYycGiLqPqGXUGuOlP8ahSOwonRwOhqTiao-1ib74oGkOQ==" # Or paste your token string here
org = "dev team"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
bucket = "readings" # Ensure this bucket exists in your InfluxDB UI

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

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
last_data = 0
rain_value = 1023

try:
    rfid.start()
    servo.pwmInit()
    buzzer.buzzInit()
    rainsensor.init(bus=0, device=1)
    lcd.clear_safe()
    
    while True:
        now = time.time()           
                
        #Temperature reading every 10 second
        if (now - last_sensor >= 10):
            bme_sensor.bmeRead()
            last_sensor = now
            
        #LCD display Temp/Hum reading every 10 second
        if (now - last_lcd >= 10):
            lcd.clear_safe()
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
        
        #Rain reading every 2 second
        if (now - last_rain >= 2):
            rain_value = rainsensor.read_adc(0)
            print("Rain ADC value:", rain_value)
            weather_status = rainsensor.is_raining() # to get weather status whether its raining or sunny
            last_rain = now
                   
        # =========================
        # InfluxDb sending of data
        # =========================            
        if (now - last_data >= 30):
            try:
                point = (
                    Point("environment")
                    .tag("id", "pi4smarthome")
                    .field("temperature", bme_sensor.data.temperature)
                    .field("humidity", bme_sensor.data.humidity)
                    .field("pressure", bme_sensor.data.pressure)
                    .field("fan", fan.fanStatus(bme_sensor.data.temperature))
                    .field("weather", weather_status)
                    .field("door", servo.doorStatus())
                    .field("window", rainsensor.window_status())
                    .field("pole", rainsensor.pole_status())
                )
                write_api.write(bucket=bucket, org=org, record=point)
                print("BME280 data sent to InfluxDB")
            except Exception as e:
                print(f"Failed to write BME280 data to InfluxDB: {e}")
            last_data = now

        fan.turn_on_fan(bme_sensor.data.temperature) #Turn on/off the fan
        servo.door_open()
        servo.window_open(rain_value)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    pass
finally:
    servo.pwmStop()
    buzzer.pwmStop()
    rainsensor.close() 
    G.cleanup()
