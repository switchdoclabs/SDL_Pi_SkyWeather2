#!/usr/bin/python
# Author: Bastien Wirtz <bastien.wirtz@gmail.com>

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

from __future__ import print_function
from bmp280 import BMP280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


# Initialise the BMP280
bus = SMBus(1)
sensor = BMP280(i2c_dev=bus, i2c_addr=0x77)


print('Temp = {0:0.2f} *C'.format(sensor.get_temperature()))
print('Pressure = {0:0.2f} Pa'.format(sensor.get_pressure()))
print('Altitude = {0:0.2f} m'.format(sensor.get_altitude()))
print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.get_sealevel_pressure(626.0)))
