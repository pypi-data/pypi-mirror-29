import os

from numpy import vstack

from .common import *

class BTIChannelHeader(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.name          = megdata_read_str(fd, 16)
        ret.chan_no       = megdata_read_int16(fd)
        ret.ctype         = megdata_read_uint16(fd)
        ret.sensor_no     = megdata_read_int16(fd)
        # Structure padding
        os.lseek(fd, 2, os.SEEK_CUR)
        ret.gain          = megdata_read_float(fd)
        ret.units_per_bit = megdata_read_float(fd)
        ret.yaxis_label   = megdata_read_str(fd, 16)
        ret.aar_val       = megdata_read_double(fd)
        ret.checksum      = megdata_read_int32(fd)
        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIChannelHeader\n'
        s += (' ' * indent) + ' Name:           %s\n' % self.name
        s += (' ' * indent) + ' Channel number: %d\n' % self.chan_no
        s += (' ' * indent) + ' Channel Type:   %d\n' % self.ctype
        s += (' ' * indent) + ' Sensor Number:  %d\n' % self.sensor_no
        s += (' ' * indent) + ' Gain:           %e\n' % self.gain
        s += (' ' * indent) + ' UPB:            %e\n' % self.units_per_bit
        s += (' ' * indent) + ' Y-Axis Label:   %s\n' % self.yaxis_label
        s += (' ' * indent) + ' AAR:            %e\n' % self.aar_val
        s += (' ' * indent) + ' Checksum:       %d\n' % self.checksum
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIDeviceHeader(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.size          = megdata_read_int32(fd)
        ret.checksum      = megdata_read_int32(fd)
        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIDeviceHeader\n'
        s += (' ' * indent) + '  Size:        %s\n' % self.size
        s += (' ' * indent) + '  Checksum:    %d\n' % self.checksum
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIMegDevice(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.hdr           = BTIDeviceHeader.from_fd(fd)
        ret.inductance    = megdata_read_float(fd)
        ret.padding       = megdata_read_str(fd, 4)
        ret.transform     = bti_read_xfm(fd)
        ret.xform_flag    = megdata_read_int16(fd)
        ret.total_loops   = megdata_read_int16(fd)
        # Padding
        os.lseek(fd, 4, os.SEEK_CUR)

        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIMegDevice\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + ' Inductance:      %e\n' % self.inductance
        s += (' ' * indent) + ' Transform:       ' + megdata_array_print(self.transform, indent + 18) + '\n'
        s += (' ' * indent) + ' XFormFlag:       %d\n' % self.xform_flag
        s += (' ' * indent) + ' Total Loops:     %d\n' % self.total_loops
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIMegLoop(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.position      = megdata_read_vec3(fd)
        ret.orientation   = megdata_read_vec3(fd)
        ret.radius        = megdata_read_double(fd)
        ret.wire_radius   = megdata_read_double(fd)
        ret.turns         = megdata_read_int16(fd)
        # Struct padding
        os.lseek(fd, 2, os.SEEK_CUR)
        ret.checksum      = megdata_read_int32(fd)
        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIMegLoop\n'
        s += (' ' * indent) + '  Position:    ' + str(self.position) + '\n'
        s += (' ' * indent) + '  Orientation: ' + str(self.orientation) + '\n'
        s += (' ' * indent) + '  Radius:      %e\n' % self.radius
        s += (' ' * indent) + '  Wire Radius: %e\n' % self.wire_radius
        s += (' ' * indent) + '  Turns:       %d\n' % self.turns
        s += (' ' * indent) + '  Checksum:    %d\n' % self.checksum
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_CHANTYPE_MEG       = 1
BTI_CHANTYPE_EEG       = 2
BTI_CHANTYPE_REFERENCE = 3
BTI_CHANTYPE_EXTERNAL  = 4
BTI_CHANTYPE_TRIGGER   = 5
BTI_CHANTYPE_UTILITY   = 6
BTI_CHANTYPE_DERIVED   = 7
BTI_CHANTYPE_SHORTED   = 8

class BTIMegChannel(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.device        = BTIMegDevice.from_fd(fd)
        ret.loops         = []
        for j in range(ret.device.total_loops):
            loop = BTIMegLoop.from_fd(fd)
            ret.loops.append( loop )
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIMegChannel\n'
        s += self.device.str_indent(indent=indent+2)
        for loop in self.loops:
            s += loop.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

    @property
    def position(self):
        return vstack([self.loops[x].position for x in range(len(self.loops))])

    @property
    def orientation(self):
        return vstack([self.loops[x].orientation for x in range(len(self.loops))])

    @property
    def radius(self):
        return vstack([self.loops[x].radius for x in range(len(self.loops))])

    @property
    def wire_radius(self):
        return vstack([self.loops[x].wire_radius for x in range(len(self.loops))])

    @property
    def turns(self):
        return vstack([self.loops[x].turns for x in range(len(self.loops))])


class BTIEegChannel(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.hdr           = BTIDeviceHeader.from_fd(fd)
        ret.impedance     = megdata_read_float(fd)
        ret.padding       = megdata_read_str(fd, 4)
        ret.transform     = bti_read_xfm(fd)
        ret.reserved      = megdata_read_char(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIEegChannel\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + '  Impedance:      %e\n' % self.impedance
        s += (' ' * indent) + '  Transform:      ' + megdata_array_print(self.transform, indent + 18) + '\n'
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIExternalDevice(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.hdr           = BTIDeviceHeader.from_fd(fd)
        ret.user_space_size = megdata_read_int32(fd)
        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIExternalDevice\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + '  UserSpaceSize: %d\n' % self.user_space_size
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTITriggerDevice(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.hdr           = BTIDeviceHeader.from_fd(fd)
        ret.user_space_size = megdata_read_int32(fd)
        # Padding
        os.lseek(fd, 2, os.SEEK_CUR)
        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTITriggerDevice\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + '  UserSpaceSize: %d\n' % self.user_space_size
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIUtilityDevice(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.hdr           = BTIDeviceHeader.from_fd(fd)
        ret.user_space_size = megdata_read_int32(fd)
        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIUtilityDevice\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + '  UserSpaceSize: %d\n' % self.user_space_size
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIDerivedDevice(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.hdr           = BTIDeviceHeader.from_fd(fd)
        ret.user_space_size = megdata_read_int32(fd)
        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIDerivedDevice\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + '  UserSpaceSize: %d\n' % self.user_space_size
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIShortedDevice(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.hdr           = BTIDeviceHeader.from_fd(fd)
        ret.reserved      = megdata_read_str(fd, 32)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIShortedDevice\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


BTI_CHANTYPES = {
        BTI_CHANTYPE_MEG:       BTIMegChannel,
        BTI_CHANTYPE_EEG:       BTIEegChannel,
        BTI_CHANTYPE_REFERENCE: BTIMegChannel,
        BTI_CHANTYPE_EXTERNAL:  BTIExternalDevice,
        BTI_CHANTYPE_TRIGGER:   BTITriggerDevice,
        BTI_CHANTYPE_UTILITY:   BTIUtilityDevice,
        BTI_CHANTYPE_DERIVED:   BTIDerivedDevice,
        BTI_CHANTYPE_SHORTED:   BTIShortedDevice
}


class BTIChannel(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        # First a channel header
        ret.hdr           = BTIChannelHeader.from_fd(fd)

        # Deal with padding
        curpos = os.lseek(fd, 0, os.SEEK_CUR);
        if ((curpos % 8) != 0):
            os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        # Then the channel info
        ret.chan          = BTI_CHANTYPES[ret.hdr.ctype].from_fd(fd)

        # Deal with padding
        curpos = os.lseek(fd, 0, os.SEEK_CUR);
        if ((curpos % 8) != 0):
            os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIChannel\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += self.chan.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


    @property
    def position(self):
        if not hasattr(self.chan, 'position'):
            raise Exception('Channel does not have position information')

        return self.chan.position

    @property
    def orientation(self):
        if not hasattr(self.chan, 'orientation'):
            raise Exception('Channel does not have orientation information')

        return self.chan.orientation

    @property
    def radius(self):
        if not hasattr(self.chan, 'radius'):
            raise Exception('Channel does not have radius information')

        return self.chan.radius

    @property
    def wire_radius(self):
        if not hasattr(self.chan, 'wire_radius'):
            raise Exception('Channel does not have wire_radius information')

        return self.chan.wire_radius

    @property
    def turns(self):
        if not hasattr(self.chan, 'turns'):
            raise Exception('Channel does not have turns information')

        return self.chan.turns
