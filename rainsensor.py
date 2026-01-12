# import spidev
# 
# spi = spidev.SpiDev()
# spi.open(0, 1)               # bus 0, CE1
# spi.max_speed_hz = 1350000   # speed for MCP3008
# 
# 
# # READ MCP3008 CHANNEL
# def read_adc(channel):
#     """
#     Read ADC value from MCP3008 (0–1023)
#     """
#     if channel < 0 or channel > 7:
#         return -1
# 
#     # MCP3008 protocol
#     adc = spi.xfer2([
#         1,                      # start bit
#         (8 + channel) << 4,     # single-ended
#         0
#     ])
# 
#     value = ((adc[1] & 3) << 8) | adc[2]
#     return value
#

import spidev

_spi = spidev.SpiDev()
_inited = False

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

    # IMPORTANT: re-assert (other modules may have changed these)
    _spi.max_speed_hz = 1350000
    _spi.mode = 0b00

    if channel < 0 or channel > 7:
        return -1

    adc = _spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) | adc[2]

def close():
    global _inited
    if _inited:
        _spi.close()
        _inited = False
