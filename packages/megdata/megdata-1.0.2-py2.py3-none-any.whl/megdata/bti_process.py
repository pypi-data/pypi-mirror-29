import os
import time

from .common import *

#############################################################################
# User process header
#############################################################################
class BTIUserProcessHeader(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ## Process Header
        ret.nbytes          = megdata_read_int32(fd)
        ret.processtype     = megdata_read_str(fd, 20)
        ret.checksum        = megdata_read_int32(fd)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIUserProcessHeader\n'
        s +=  (' ' * indent) + '  NBytes:           %d\n' % self.nbytes
        s +=  (' ' * indent) + '  ProcessType:      %s\n' % self.processtype
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIGenUserProcess(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.user_space_size  = megdata_read_int32(fd)
        # Structure padding
        os.lseek(fd, 32, os.SEEK_CUR)

        # Now store the user space data somewhere
        # we can read it
        ret.user_data = os.read(fd, ret.user_space_size)

        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIGenUserProcess\n'
        s +=  (' ' * indent) + '  User Space Size:  %d\n' % self.user_space_size
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTINoiseProcess(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.user_space_size  = megdata_read_int32(fd)
        # Structure padding
        os.lseek(fd, 32, os.SEEK_CUR)

        # Now grab the noise data
        ret.noise = megdata_read_double(fd, count=ret.user_space_size/8)

        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTINoiseProcess\n'
        s += (' ' * indent) + '  Noise data:        %d entries\n' % len(self.noise)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIFilterProcess(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.frequency       = megdata_read_float(fd)

        # Structure padding
        os.lseek(fd, 32, os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIFilterProcess\n'
        s += (' ' * indent) + '  Frequency:        %f\n' % self.frequency
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIBandFilterProcess(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.high_freq       = megdata_read_float(fd)
        ret.low_freq        = megdata_read_float(fd)

        # Structure padding
        os.lseek(fd, 32, os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIBandFilterProcess\n'
        s += (' ' * indent) + '  High Frequency:   %f\n' % self.high_freq
        s += (' ' * indent) + '  Low Frequency:    %f\n' % self.low_freq
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIDefaultProcess(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.scaleoption     = megdata_read_int32(fd)
        # Structure padding
        os.lseek(fd, 4, os.SEEK_CUR)
        ret.scale           = megdata_read_double(fd)
        ret.dtype           = megdata_read_int32(fd)
        ret.selected        = megdata_read_int16(fd)
        ret.colordisplay    = megdata_read_int16(fd)
        # Structure padding - no idea why
        os.lseek(fd, 32, os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIDefaultProcess\n'
        s += (' ' * indent) + '  Scale Option:     %d\n' % self.scaleoption
        s += (' ' * indent) + '  Scale             %f\n' % self.scale
        s += (' ' * indent) + '  Type:             %d\n' % self.dtype
        s += (' ' * indent) + '  Selected:         %d\n' % self.selected
        s += (' ' * indent) + '  Color Display:    %d\n' % self.colordisplay
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIUserProcess(object):
    @classmethod
    def from_fd(cls, fd, bti_def=False):
        ret = cls()

        ret.hdr             = BTIUserProcessHeader.from_fd(fd)
        if bti_def:
            ret.data = BTIDefaultProcess.from_fd(fd)
        else:
            if ret.hdr.processtype in ['b_filt_hp', 'b_filt_lp', 'b_filt_notch']:
                ret.data = BTIFilterProcess.from_fd(fd)
            elif ret.hdr.processtype in ['b_filt_b_pass', 'b_filt_b_reject']:
                ret.data = BTIBandFilterProcess.from_fd(fd)
            elif ret.hdr.processtype in ['b_noise']:
                ret.data = BTINoiseProcess.from_fd(fd)
            else:
                ret.data = BTIGenUserProcess.from_fd(fd)

        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIUserProcess\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += self.data.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

#############################################################################
# User process wrapper class
#############################################################################
class BTIProcess(object):
    @classmethod
    def from_fd(cls, fd, processes=None):
        ret = cls()

        # Process header
        ret.hdr = BTIUserProcessHeader.from_fd(fd)

        ret.user           = megdata_read_str(fd, 32)
        ret.timestamp      = megdata_read_int32(fd)
        ret.filename       = megdata_read_str(fd, 256)
        ret.total_steps    = megdata_read_int32(fd)

        # Structure padding
        os.lseek(fd, 32, os.SEEK_CUR)

        # Deal with padding
        curpos = os.lseek(fd, 0, os.SEEK_CUR);
        if ((curpos % 8) != 0):
            os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        ret.steps = []
        for s in range(ret.total_steps):
            if ret.hdr.processtype == 'BTi_defaults':
                st = BTIUserProcess.from_fd(fd, bti_def=True)
            else:
                st = BTIUserProcess.from_fd(fd)
            ret.steps.append(st)

            curpos = os.lseek(fd, 0, os.SEEK_CUR);
            if ((curpos % 8) != 0):
                os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIUserProcess\n'
        s += self.hdr.str_indent(indent=indent+2)
        s +=  (' ' * indent) + '  User:             %s\n' % self.user
        s +=  (' ' * indent) + '  Timestamp:        %s (%d)\n' % (time.ctime(self.timestamp), self.timestamp)
        s +=  (' ' * indent) + '  Filename:         %s\n' % self.filename
        s +=  (' ' * indent) + '  Total Steps:      %s\n' % self.total_steps
        for st in self.steps:
            s += st.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

