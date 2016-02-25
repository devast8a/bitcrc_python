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

    def generate(self, data, length = None):
        """
            Return a checksum for a given list of bytes

            You may optionally specify the length of the message (in bits),
            otherwise the entire list of bytes will be used.
        """

        if length == None:
            # Length in bytes
            bytes = len(data)
            # Remaining length in bits
            bits = 0
        else:
            length = min(len(data) * 8, length)
            lastByte = data[(length / 8)]
            bytes = length / 8
            bits = length % 8

        offset = 0
        crc = self.initialValue
        table = self.table

        while offset < bytes:
            # Get the top byte of crc
            topByte = (crc >> self.SHIFT_TOP_BYTE) & 0xFF
            crc = (crc & self.MASK_SHIFT_BY_BYTE) << 8
            crc ^= table[topByte ^ data[offset]]
            offset += 1

        # Handle message lengths that are a non-multiple of 8
        #   by processing the remaining bits.
        for bit in range(bits):
            topBit = (lastByte & 0x80) ^ ((crc >> self.SHIFT_TOP_BYTE) & 0x80)
            crc = (crc & self.MASK_SHIFT_BY_BIT) << 1
            lastByte <<= 1

            if topBit:
                crc ^= self.polynomial

        if self.reverseOut:
            crc = reverse(crc, self.order)

        return crc ^ self.xorOut
