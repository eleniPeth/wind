import spidev
import RPi.GPIO as GPIO
import time
import csv

# Global handles
_spi = None
_pwm = None

R1 = 230   # top resistor (Ω)
R2 =  10   # bottom resistor (Ω)
DIV_INV = (R1 + R2) / R2



def init_adc(bus=0, device=0, max_speed_hz=1000000):
    """
    Initialize SPI for MCP3208.
    bus, device: SPI bus and chip select
    max_speed_hz: SPI clock speed
    """
    global _spi
    _spi = spidev.SpiDev()
    _spi.open(bus, device)
    _spi.max_speed_hz = max_speed_hz

def _read_channel(channel):
    """
    Low-level read from MCP3208 channel (0-7).
    Returns raw ADC code (0-4095).
    """
    # Command bits: start=1, single-ended=1, channel bits
    cmd = 0x06 | ((channel & 4) >> 2)
    msb = ((channel & 3) << 6)
    adc = _spi.xfer([cmd, msb, 0])
    data = ((adc[1] & 15) << 8) | adc[2]
    return data

def read_voltage(channel, vref=5.0):
    raw = _read_channel(channel)  
    return (raw / 4095.0) * vref

def read_current(channel, vref=5.0):
    adc_value = _read_channel(channel)
    current = (adc_value) * (vref/(4095 * 0.0625))
    return current
    

def shutdown():
    """
    Clean up SPI and GPIO.
    """
    global _spi, _pwm
    if _pwm:
        _pwm.stop()
    GPIO.cleanup()
    if _spi:
        _spi.close()




# Initialize ADC
init_adc(bus=0, device=0, max_speed_hz=100000)


next_time = time.time()
step = 0

try:
    while True:
        # Reading
        measured_vout = read_voltage(channel=1, vref=5.0) * DIV_INV
        vin = read_voltage(channel=2, vref=5.0) * DIV_INV
        current = helpers.read_current(channel=3, vref=5.0) * DIV_INV

            
            
        step += 1

        # Timing control
        next_time += Ts
        sleep = next_time - time.time()
        if sleep > 0:
            time.sleep(sleep)
        else:
            next_time = time.time()

except KeyboardInterrupt:
    print("Stopping…")
finally:
    #csvfile.close()
    shutdown()
