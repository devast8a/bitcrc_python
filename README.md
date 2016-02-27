# bitcrc
Perform CRC with arbitrary order polynomials on data with an arbitrary length accelerated with lookup tables.

# Why?
1. You need to support a polynomial that's not a multiple of 8 bits long.
2. You need to support data that's not a multiple of 8 bits long.
3. It needs to be relatively fast.

# How?
You can use the BitCrc class directly
```python
from bitcrc_python import BitCrc

# Our polynomial is 0x1021, 16 bits long
crc = BitCrc(16, 0x1021, initialValue=0xFFFF, xorOut=0xFFFF)
checksum = crc.generate("Hello World")
assert(checksum == 0x4D25)
```

Or drop the library in as a replacement for crcmod
```python
from bitcrc_python import crcmod

# Instead of specifying the length with crcmod
#   you just need to include the leading bit.
crc = crcmod.mkCrcFun(0x11021, initCrc=0xFFFF)
checksum = crc("Hello world")
assert(checksum == 0x4D25)
```

# License
This library is licensed under MIT.
