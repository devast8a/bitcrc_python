def set(bit):
    """Set the specifeid bit eg. set(8) == 0x80"""
    return 1 << (bit - 1)

def setN(n):
    """Set the first n specified bits eg. setN(7) == 0x7F"""
    return set(n + 1) - 1

def reverse(value, length):
    output = 0
    for bit in range(length):
        if value & set(bit + 1) != 0:
            output |= set(length - bit)
    return output

