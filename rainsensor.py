import spidev

spi = spidev.SpiDev()
spi.open(0, 1)               # bus 0, CE0
spi.max_speed_hz = 1350000   # safe speed for MCP3008

# -------------------------
# READ MCP3008 CHANNEL
# -------------------------
def read_adc(channel):
    """
    Read ADC value from MCP3008 (0–1023)
    """
    if channel < 0 or channel > 7:
        return -1

    # MCP3008 protocol
    adc = spi.xfer2([
        1,                      # start bit
        (8 + channel) << 4,     # single-ended
        0
    ])

    value = ((adc[1] & 3) << 8) | adc[2]
    return value

