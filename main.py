import RPi.GPIO as G 
import bme_sensor, fan

G.setwarnings(False)
G.setmode(G.BCM)
G.setup(17,G.OUT)

try:
    bme_sensor.bmeRead() #Temperature reading every 2 second
    while True:
        fan.turn_on_fan(bme_sensor.data.temperature) #Turn on/off the fan
except KeyboardInterrupt:
    pass
finally:
    G.cleanup()
        