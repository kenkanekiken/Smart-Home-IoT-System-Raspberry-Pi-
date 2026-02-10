🏠 Smart Home IoT System (Raspberry Pi)
Video of Prototype: https://youtube.com/shorts/vM1uQvEnK7M?si=o_nDKT4kMYFRyJoW 

A Raspberry Pi–based smart home automation system that monitors environmental conditions and controls multiple household devices automatically and manually. The system integrates various sensors and actuators, including a BME280 environmental sensor, rain sensor, RFID access control, LCD display, servo motors, and a fan controlled via GPIO.

The project is designed using a modular and scalable architecture, allowing easy expansion for additional smart home features and IoT services.

Features

🌡 Real-time temperature, humidity, and pressure monitoring (BME280)
Automatic fan control based on temperature thresholds
🌧 Rain detection to trigger automated actions (e.g. window control)
RFID access control using RC522 (door simulation)
⚙️ Servo motor control for doors, windows, or mechanisms
📟 LCD display for live system status and sensor readings
Modular Python-based architecture
GPIO, I2C, and SPI hardware integration


System Architecture
                ┌──────────────┐
                │   BME280     │
                │ (Temp/Hum)   │
                └──────┬───────┘
                       │ I2C
                ┌──────▼───────┐
                │  Rain Sensor │
                └──────┬───────┘
                       │ GPIO
┌─────────┐ SPI ┌──────▼───────┐
│ RFID    │────▶│ Raspberry Pi │◀── I2C ── LCD
│ RC522   │     │  Controller  │
└─────────┘     └──────┬───────┘
                       │ GPIO / PWM
              ┌────────▼────────┐
              │ Fan / Servo(s)  │
              └─────────────────┘



🛠 Hardware Requirements

Raspberry Pi (3 / 4 / 5)
BME280 Temperature, Humidity & Pressure Sensor (I2C)
Rain Sensor Module (Digital / Analog)
RFID RC522 Module (SPI)
Servo Motor(s)
Relay Module or GPIO-controlled fan
LCD Display (I2C)
Jumper wires


📦 Software Requirements

Raspberry Pi OS
Python 3
Required Python libraries:
pip3 install smbus2 RPi.bme280 mfrc522 RPi.GPIO

Enable:
I2C
SPI
GPIO (default enabled)


Project Structure 
smarthome/
│
├── bme_sensor.py     # BME280 sensor readings
├── rain_sensor.py    # Rain detection logic
├── rfid.py           # RFID RC522 access control
├── fan.py            # Fan control (GPIO / relay)
├── servo.py          # Servo motor control
├── lcd.py            # LCD display handling
├── main.py           # Main system controller
└── README.md


▶️ How It Works

Environmental data is collected from the BME280 sensor.
Rain sensor detects rainfall to trigger automated actions.
RFID RC522 authenticates users for access control.
Servo motors simulate doors, windows, or mechanical actions.
The LCD displays live sensor readings and system status.
The fan is automatically activated when temperature exceeds a set threshold.
The main controller coordinates all modules in real time.


Future Improvements

Add hysteresis to prevent frequent fan toggling
Integrate MQTT for remote monitoring and control
Web or mobile dashboard
Cloud logging and alerts
User management for RFID access
AI-based environment prediction


🎓 Educational Purpose

This project demonstrates practical IoT and embedded systems concepts, including:
Sensor interfacing (I2C, SPI, GPIO)
Actuator control (relay, servo, fan)
Modular Python programming
Smart home automation logic
Real-time system integration

License
This project is intended for educational and learning purposes.
