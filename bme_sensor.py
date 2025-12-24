import bme280
import smbus2

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

def bmeRead():
    global data
    data = bme280.sample(bus, address, calibration_params)
    print(f"Temp: {data.temperature:.2f}  Hum: {data.humidity:.2f}  Pres: {data.pressure:.2f}")