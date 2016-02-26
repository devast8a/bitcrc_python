# This file provides support for BitCrc to act as a drop-in replacement for
# crcmod

from BitCrc import BitCrc
import math
import bits
import struct

def mkCrcFun(poly, initCrc=None, rev=True, xorOut=0):
    # reverse isn't supported at the moment

    # Find order and unset leading bit
    order = bits.find_last_set(poly) - 1
    poly ^= 1 << order

    # crcmod defaults initCrc to all bits set
    if initCrc == None:
        initCrc = bits.setN(order)

    crc_generator = BitCrc(
        order,
        poly,
        initialValue = initCrc,
        xorOut = xorOut,
        reverseData = rev
    )

    def calculate(data):
        return crc_generator.generate(data)

    return calculate

class Crc(object):
    def __init__(self, poly, initCrc=0, rev=True, xorOut=0):
        order = bits.find_last_set(poly) - 1
        poly ^= 1 << order

        self.crc_generator = BitCrc(
            order,
            poly,
            initialValue = initCrc,
            xorOut = xorOut
        )

        self.digest_size = math.ceil(order / 4)
        self.crcValue = initCrc ^ xorOut

    def new(self, arg = None):
        other = Crc.__new__(Crc)
        other.crc_generator = self.crc_generator
        other.crcValue = self.crc_generator.initialValue

    def copy(self):
        other = self.new()
        other.crcValue = self.crcValue

    def update(self, data):
        if type(data) == str:
            data = struct.unpack("%dB" % len(data), data)

        self.crcValue ^= self.crc_generator.xorOut

        for byte in data:
            self.crcValue = self.crc_generator.update_byte(self.crcValue, byte)

        self.crcValue ^= self.crc_generator.xorOut
