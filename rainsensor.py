import spidev

_spi = spidev.SpiDev()
_inited = False

weather = None
window_status = None
pole_status = None

def init(bus=0, device=1, speed=1350000):
    global _inited
    if not _inited:
        _spi.open(bus, device)      # device 0=CE0, 1=CE1
        _spi.max_speed_hz = speed
        _spi.mode = 0b00
        _inited = True

def read_adc(channel):
    if not _inited:
        init()

    _spi.max_speed_hz = 1350000
    _spi.mode = 0b00

    if channel < 0 or channel > 7:
        return -1

    adc = _spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) | adc[2]
                
def is_raining():
    is_raining = read_adc(0) < 500
    if is_raining:
        weather = "Raining"
    else:
        weather = "Sunny"
    return weather

def window_status():
    is_raining = read_adc(0) < 500
    if is_raining:
        window_status = "Close"
    else:
        window_status = "Open"
    return window_status

def pole_status():
    is_raining = read_adc(0) < 500
    if is_raining:
        pole_status = "Retract"
    else:
        pole_status = "Extend"
    return pole_status       
    
def close():
    global _inited
    if _inited:
        _spi.close()
        _inited = False
