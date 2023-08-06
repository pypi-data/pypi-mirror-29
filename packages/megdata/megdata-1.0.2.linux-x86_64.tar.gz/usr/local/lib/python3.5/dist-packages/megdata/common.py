import os
import struct

import numpy

__all__ = []

def megdata_read_bytes(fd, delimiter='\n'):
    """
    Reads bytes until the character matching delimiter is hit
    """
    ret = ''
    while True:
        val = os.read(fd, 1)
        if val == delimiter:
            break

        ret += val

    return ret

__all__.append('megdata_read_bytes')

def megdata_read_str(fd, count=1):
    fmt = '>' + ('c' * count)
    dat = list(struct.unpack(fmt, os.read(fd, struct.calcsize(fmt))))

    # Sort out NUL termination
    dat = b''.join(dat)
    try:
        l = dat.index(b'\x00')
    except ValueError:
        l = count

    return dat[0:l].decode('ascii')

__all__.append('megdata_read_str')

def megdata_read_char(fd, count=1):
    fmt = '>' + ('c' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_char')

def megdata_read_bool(fd, count=1):
    fmt = '>' + ('?' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_bool')

def megdata_read_uint8(fd, count=1):
    fmt = '>' + ('B' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_uint8')

def megdata_read_int8(fd, count=1):
    fmt = '>' + ('b' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_int8')

def megdata_read_uint16(fd, count=1):
    fmt = '>' + ('H' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_uint16')

def megdata_read_int16(fd, count=1):
    fmt = '>' + ('h' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_int16')

def megdata_read_uint32(fd, count=1):
    fmt = '>' + ('I' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_uint32')

def megdata_read_int32(fd, count=1):
    fmt = '>' + ('i' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_int32')

def megdata_read_uint64(fd, count=1):
    fmt = '>' + ('Q' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_uint64')

def megdata_read_int64(fd, count=1):
    fmt = '>' + ('q' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_int64')

def megdata_read_float(fd, count=1):
    fmt = '>' + ('f' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_float')

def megdata_read_double(fd, count=1):
    fmt = '>' + ('d' * count)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    if count == 1:
        return dat[0]
    else:
        return list(dat)

__all__.append('megdata_read_double')

def megdata_read_int16_matrix(fd, rows, cols):
    ret = numpy.zeros((rows, cols), numpy.int16)
    fmt = '>' + ('h' * rows * cols)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    m = 0
    for j in range(rows):
        for k in range(cols):
            ret[j][k] = dat[m]
            m += 1
    return ret

__all__.append('megdata_read_int16_matrix')

def megdata_read_float_matrix(fd, rows, cols):
    ret = numpy.zeros((rows, cols), numpy.float32)
    fmt = '>' + ('f' * rows * cols)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    m = 0
    for j in range(rows):
        for k in range(cols):
            ret[j][k] = dat[m]
            m += 1
    return ret

__all__.append('megdata_read_float_matrix')

def megdata_read_double_matrix(fd, rows, cols):
    ret = numpy.zeros((rows, cols), numpy.float64)
    fmt = '>' + ('d' * rows * cols)
    dat = struct.unpack(fmt, os.read(fd, struct.calcsize(fmt)))
    m = 0
    for j in range(rows):
        for k in range(cols):
            ret[j][k] = dat[m]
            m += 1
    return ret

__all__.append('megdata_read_double_matrix')

def megdata_read_vec3(fd, count=1):
    return megdata_read_double_matrix(fd, count, 3)

__all__.append('megdata_read_vec3')

def megdata_read_vec4(fd, count=1):
    return megdata_read_double_matrix(fd, count, 4)

__all__.append('megdata_read_vec4')

# These ones are BTI-style specific so name that way
def bti_read_xfm(fd):
    return megdata_read_double_matrix(fd, 4, 4)

__all__.append('bti_read_xfm')

def bti_read_rot(fd):
    return megdata_read_double_matrix(fd, 3, 3)

__all__.append('bti_read_rot')

def megdata_array_print(array, indent=0):
    s = str(array)
    s = s.replace('\n', '\n' + ' ' * indent)
    return s

__all__.append('megdata_array_print')
