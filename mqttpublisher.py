import time
import paho.mqtt.client as mqtt
import bme_sensor
import random

mqtt_broker = "test.mosquitto.org"
topic = "smarthome/latest"

while True:
	data = bme_sensor.bmeRead()
	temp = "Temperature: " + str(data.temperature)

	my_mqtt = mqtt.Client()
	print("\nCreated client object at " + time.strftime("%H:%M:%S"))

	my_mqtt.connect(mqtt_broker, port=1883)
	print("connected to broker")

	try:
		my_mqtt.publish(topic, temp)
	except:
		print("Error publishing")
	else:
		my_mqtt.disconnect()
		print("Disconnected from broker")
