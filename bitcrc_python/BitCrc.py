import bits

class BitCrc:
    def __init__(self, order, polynomial, initialValue = 0, xorOut = 0, reverseOut = False):

        # The amount to shift right to move the top byte to the bottom byte
        self.SHIFT_TOP_BYTE     = order - 8
        # Mask out everything but the top bit
        self.MASK_TOPBIT        = bits.set(order)
        # Mask used when shifting left by a BIT
        self.MASK_SHIFT_BY_BIT  = bits.setN(order - 1)
        # Mask used when shifting left by a BYTE
        self.MASK_SHIFT_BY_BYTE = bits.setN(order - 8)

        self.order        = order
        self.polynomial   = polynomial
        self.initialValue = initialValue
        self.table        = self.create_table()
        self.xorOut       = xorOut
        self.reverseOut   = reverseOut

    def create_table(self):
        """
            Return a precomputed CRC table
        """
        return [self.create_table_entry(byte) for byte in range(0,256)]

    def create_table_entry(self, byte):
        """
            Return a CRC table entry for a given control byte
        """
        crc = (byte << self.SHIFT_TOP_BYTE)

        for bit in range(8):
            topBit = (crc & self.MASK_TOPBIT)
            crc = (crc & self.MASK_SHIFT_BY_BIT) << 1
            if topBit:
                crc ^= self.polynomial

        return crc

    def update_byte(self, initial, byte):
        """
            Calculate a checksum from an initial checksum and a byte of data
        """
        topByte = (initial >> self.SHIFT_TOP_BYTE) & 0xFF
        initial = (initial & self.MASK_SHIFT_BY_BYTE) << 8
        return initial ^ self.table[topByte ^ byte]

    def update_bits(self, initial, byte, length):
        """
            Calculate a checksum from an initial checksum and a byte of data.
            Only uses a number of bits specified by length.
        """
        for bit in range(length):
            topBit = (byte & 0x80) ^ ((initial >> self.SHIFT_TOP_BYTE) & 0x80)
            initial = (initial & self.MASK_SHIFT_BY_BIT) << 1
            byte <<= 1

            if topBit:
                initial ^= self.polynomial
        return initial

    def generate(self, data, length = None):
        """
            Return a checksum for a given list of bytes

            You may optionally specify the length of the message (in bits),
            otherwise the entire list of bytes will be used.
        """

        if length == None:
            # Length in bytes
            totalBytes = len(data)
            # Remaining length in bits
            remainingBits = 0
        elif length > len(data) * 8:
            raise ValueError("length is longer than the length of given data")
        else:
            totalBytes = length / 8
            remainingBits = length % 8

        offset = 0
        crc = self.initialValue

        while offset < totalBytes:
            crc = self.update_byte(crc, data[offset])
            offset += 1

        if remainingBits > 0:
            crc = self.update_bits(crc, data[totalBytes], remainingBits)

        if self.reverseOut:
            crc = bits.reverse(crc, self.order)

        return crc ^ self.xorOut
