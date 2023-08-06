import os

from .common import *
from .bti_userblocks import *
from .bti_channel import *

BTI_SYSTYPES = {
        4: 'WHS2500M', # WHS2500 magnetometers
        5: 'WHS2500G', # WHS2500 gradiometers
        7: 'WHS3600M', # WHS3600 magnetometers
        8: 'WHS3600G', # WHS3600 gradiometers
}

class BTIConfigHeader(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.version            = megdata_read_int16(fd)
        ret.sitename           = megdata_read_str(fd, 32)
        ret.dap_hostname       = megdata_read_str(fd, 16)
        ret.sys_type           = megdata_read_int16(fd)
        ret.sys_options        = megdata_read_int32(fd)
        ret.supply_freq        = megdata_read_int16(fd)
        ret.total_chans        = megdata_read_int16(fd)
        ret.system_fixed_gain  = megdata_read_float(fd)
        ret.volts_per_bit      = megdata_read_float(fd)
        ret.total_sensors      = megdata_read_int16(fd)
        ret.total_user_blocks  = megdata_read_int16(fd)
        ret.next_der_chan_no   = megdata_read_int16(fd)
        # Structure padding
        os.lseek(fd, 2, os.SEEK_CUR)
        ret.checksum           = megdata_read_uint32(fd)
        ret.reserved           = megdata_read_char(fd, 32)
        return ret

    def get_systype_string(self):
        """
        :rtype: str containing model name or empty string if unknown
        """
        return BTI_SYSTYPES.get(self.sys_type, '')

    def str_indent(self, indent=0):
        s = ''
        s += (' ' * indent) + '<BTIConfigHeader\n'
        s += (' ' * indent) + '  Version:           %d\n' % self.version
        s += (' ' * indent) + '  Sitename:          %s\n' % self.sitename
        s += (' ' * indent) + '  DAP Hostname:      %s\n' % self.dap_hostname
        s += (' ' * indent) + '  System Type:       %d\n' % self.sys_type
        s += (' ' * indent) + '  System Options:    %d\n' % self.sys_options
        s += (' ' * indent) + '  Supply Freq:       %d\n' % self.supply_freq
        s += (' ' * indent) + '  Total Chans:       %d\n' % self.total_chans
        s += (' ' * indent) + '  System Fixed Gain: %e\n' % self.system_fixed_gain
        s += (' ' * indent) + '  Volts Per Bit:     %e\n' % self.volts_per_bit
        s += (' ' * indent) + '  Total Sensors:     %d\n' % self.total_sensors
        s += (' ' * indent) + '  Total User Blocks: %d\n' % self.total_user_blocks
        s += (' ' * indent) + '  Next Der Chan No:  %d\n' % self.next_der_chan_no
        s += (' ' * indent) + '  Checksum:          %d\n' % self.checksum
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIConfigFile(object):
    @classmethod
    def from_file(cls, filename):
        """
        Read a BTI-style config file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        # First of all, we have a BTIConfigHeader
        ret.hdr         = BTIConfigHeader.from_fd(fd)

        # Now one transform per sensor
        ret.transforms  = []
        for s in range(ret.hdr.total_sensors):
            ret.transforms.append( bti_read_xfm(fd) )

        # Now read the user blocks
        ret.user_blocks = []
        for b in range(ret.hdr.total_user_blocks):
            ret.user_blocks.append( BTIUserBlock.from_fd(fd, ret.user_blocks) )

        # Finally, the channel information
        ret.channels = []
        for c in range(ret.hdr.total_chans):
            ch = BTIChannel.from_fd(fd)
            ret.channels.append(ch)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIConfigFile\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + '  Transforms:\n'
        for t in self.transforms:
            s += (' ' * (indent + 4)) + megdata_array_print(t, indent=indent+4) + '\n'

        s += (' ' * indent) + '  User Blocks:\n'
        for b in self.user_blocks:
            s += b.str_indent(indent=indent+4) + '\n'

        s += (' ' * indent) + '  Channels:\n'
        for c in self.channels:
            s += c.str_indent(indent=indent+4) + '\n'

        s += (' ' * indent) + '>'
        return s

    def __str__(self):
        return self.str_indent()


    def channel(self, chan_label):
        ret = None
        for e in self.channels:
            if e.hdr.name == chan_label:
                # Check for multiple channels and raise an error
                if ret is not None:
                    raise Exception('Multiple channels with name %s found' % chan_label)
                ret = e
        return ret
