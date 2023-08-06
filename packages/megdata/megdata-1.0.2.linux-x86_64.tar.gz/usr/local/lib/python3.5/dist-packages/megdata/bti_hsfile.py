import os
import time

from .common import *

class BTIHSFile(object):
    @classmethod
    def from_file(cls, filename):
        """
        Read a BTI-style headshape file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        # Header first
        ret.version        = megdata_read_uint32(fd)
        ret.timestamp      = megdata_read_int32(fd)
        ret.checksum       = megdata_read_int32(fd)
        ret.num_dig_points = megdata_read_int32(fd)

        # Index points
        ret.idx_points     = megdata_read_vec3(fd, 5)

        # Digitisation points
        ret.dig_points     = megdata_read_vec3(fd, ret.num_dig_points)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIHSFile\n'
        s += (' ' * indent) + '  Version:        %s\n' % self.version
        s += (' ' * indent) + '  Timestamp:      %s (%d)\n' % (time.ctime(self.timestamp), self.timestamp)
        s += (' ' * indent) + '  Num dig points: %s\n' % self.num_dig_points
        s += (' ' * indent) + '  Index points:   ' + megdata_array_print(self.idx_points, indent=indent+18) + '\n'
        s += (' ' * indent) + '  Dig points:     ' + megdata_array_print(self.dig_points, indent=indent+18) + '\n'
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()
