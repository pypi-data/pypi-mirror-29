#
# This file is part of MicroPython MPU9250 driver
# Copyright (c) 2018 Mika Tuupola
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#
# Project home:
#   https://github.com/tuupola/micropython-mpu9250
#

"""
MicroPython I2C driver for AK8963 magnetometer
"""

__version__ = "0.1.0-dev"

import ustruct # pylint: disable=import-error
from machine import I2C, Pin # pylint: disable=import-error
from micropython import const # pylint: disable=import-error

_WIA = const(0x00)
_HXL = const(0x03)
_HXH = const(0x04)
_HYL = const(0x05)
_HYH = const(0x06)
_HZL = const(0x07)
_HZH = const(0x08)
_ST2 = const(0x09)
_CNTL1 = const(0x0a)

MODE_POWER_DOWN = 0b00000000
MODE_SINGLE_MEASURE = 0b00000001
MODE_CONTINOUS_MEASURE_1 = 0b00000010 # 8Hz
MODE_CONTINOUS_MEASURE_2 = 0b00000110 # 100Hz
MODE_EXTERNAL_TRIGGER_MEASURE = 0b00000100
MODE_SELF_TEST = 0b00001000
MODE_FUSE_ROM_ACCESS = 0b00001111

OUTPUT_14_BIT = 0b00000000
OUTPUT_16_BIT = 0b00010000

_SO_14BIT = 0.6 # μT per digit when 14bit mode
_SO_16BIT = 0.15 # μT per digit when 16bit mode

class AK8963:
    """Class which provides interface to AK8963 magnetometer."""
    def __init__(
        self, i2c, address=0x0c,
        mode=MODE_CONTINOUS_MEASURE_1, output=OUTPUT_16_BIT
    ):
        self.i2c = i2c
        self.address = address

        if 0x48 != self.whoami:
            raise RuntimeError("AK8963 not found in I2C bus.")

        self._register_char(_CNTL1, (mode | output))

        if output is OUTPUT_16_BIT:
            self._so = _SO_16BIT
        else:
            self._so = _SO_14BIT

    @property
    def magnetic(self):
        """
        X, Y, Z axis micro-Tesla (uT) as floats.
        """
        so = self._so

        x = self._register_word(_HXL) * so
        y = self._register_word(_HYL) * so
        z = self._register_word(_HZL) * so
        self._register_char(_ST2) # Enable updating readings
        return (x, y, z)

    @property
    def whoami(self):
        """ Value of the whoami register. """
        return self._register_char(_WIA)

    def _register_word(self, register, value=None):
        if value is None:
            data = self.i2c.readfrom_mem(self.address, register, 2)
            return ustruct.unpack("<h", data)[0]
        data = ustruct.pack("<h", value)
        return self.i2c.writeto_mem(self.address, register, data)

    def _register_char(self, register, value=None):
        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        data = ustruct.pack("<b", value)
        return self.i2c.writeto_mem(self.address, register, data)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass