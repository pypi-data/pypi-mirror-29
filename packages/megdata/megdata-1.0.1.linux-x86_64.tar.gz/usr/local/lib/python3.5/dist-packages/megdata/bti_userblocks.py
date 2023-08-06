import os
import time

from .common import *

from numpy import zeros, int16, float

BTI_USERBLOCKS = { }

#############################################################################
# B_Mag_Info structures
#############################################################################

class BTIMagInfoBlockHeader(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        # MagInfo header structure
        ret.name          = megdata_read_str(fd, 16)
        ret.transform     = bti_read_xfm(fd)
        ret.units_per_bit = megdata_read_float(fd)
        # Structure padding
        os.lseek(fd, 20, os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIMagInfoBlockHeader\n'
        s += (' ' * indent) + '  Name:           %s\n' % self.name
        s += (' ' * indent) + '  Transform:      ' + megdata_array_print(self.transform, indent + 18) + '\n'
        s += (' ' * indent) + '  Units per Bit:  %e\n' % self.units_per_bit
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIMagInfoBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        ret.version           = megdata_read_int32(fd)
        # Structure padding
        os.lseek(fd, 20, os.SEEK_CUR)

        ret.headers = []
        for j in range(6):
            ret.headers.append( BTIMagInfoBlockHeader.from_fd(fd) )

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIMagInfoBlock\n'
        s += (' ' * indent) + '  Version:        %d\n' % self.version
        for h in self.headers:
            s += h.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return s

BTI_USERBLOCKS['B_Mag_Info'] = BTIMagInfoBlock

#############################################################################
# COH point structures
#############################################################################

class BTICOHBlockPoint(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.pos           = megdata_read_vec3(fd)
        ret.direction     = megdata_read_vec3(fd)
        ret.error         = megdata_read_double(fd)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTICOHBlockPoint\n'
        s += (' ' * indent) + '  Position:       ' + megdata_array_print(self.pos, indent + 18) + '\n'
        s += (' ' * indent) + '  Direction:      ' + megdata_array_print(self.direction, indent + 18) + '\n'
        s += (' ' * indent) + '  Error:          %s\n' % self.error
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTICOHBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()
        ret.num_points     = megdata_read_int32(fd)
        ret.status         = megdata_read_int32(fd)
        ret.points = []
        for p in range(16):
            ret.points.append (BTICOHBlockPoint.from_fd(fd))

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTICOHBlock\n'
        s += (' ' * indent) + '  Num points:     %d\n' % self.num_points
        # TODO: CONSTANTS FOR DEFINING STATUS
        s += (' ' * indent) + '  Status:         %d\n' % self.status
        for p in range(self.num_points):
            s += self.points[p].str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_COH_Points'] = BTICOHBlock

#############################################################################
# CCP XFM structures
#############################################################################

class BTICCPXFMBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()
        ret.method        = megdata_read_int32(fd)
        # Structure padding
        os.lseek(fd, 4, os.SEEK_CUR)
        ret.transform     = bti_read_xfm(fd)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTICCPXFMBlock\n'
        # TODO: CONSTANTS FOR DEFINING METHOD
        s += (' ' * indent) + '  Method:         %d\n' % self.method
        s += (' ' * indent) + '  Transform:      ' + megdata_array_print(self.transform, indent=indent+18) + '\n'
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['b_ccp_xfm_block'] = BTICCPXFMBlock

#############################################################################
# Electrode location structures
#############################################################################

class BTIElectrodeEntry(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.label         = megdata_read_str(fd, 16)
        ret.location      = megdata_read_vec3(fd)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIElectrodeEntry\n'
        s += (' ' * indent) + '  Location:       %s\n' % self.label
        s += (' ' * indent) + '  Direction:      ' + megdata_array_print(self.location, indent + 18) + '\n'
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIElectrodeBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        ret.electrodes = []
        while True:
            e = BTIElectrodeEntry.from_fd(fd)
            if e.label == '':
                break
            ret.electrodes.append(e)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIElectrodeBlock\n'
        for e in self.electrodes:
            s += e.str_indent(indent=indent + 2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['b_eeg_elec_locs'] = BTIElectrodeBlock

#############################################################################
# Hardware configuration blocks
#############################################################################

class BTIChanConfig(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.subsys_type          = megdata_read_int16(fd)
        ret.subsys_num           = megdata_read_int16(fd)
        ret.card_num             = megdata_read_int16(fd)
        ret.chan_num             = megdata_read_int16(fd)
        ret.recdspnum            = megdata_read_int16(fd)
        # Structure Padding
        os.lseek(fd, 8, os.SEEK_CUR)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIChanConfig\n'
        # TODO: CONSTANTS FOR ALL OF THESE
        s += (' ' * indent) + '  Subsys Type:    %d\n' % self.subsys_type
        s += (' ' * indent) + '  Subsys Num:     %d\n' % self.subsys_num
        s += (' ' * indent) + '  Card Num:       %d\n' % self.card_num
        s += (' ' * indent) + '  Channel Num:    %d\n' % self.chan_num
        s += (' ' * indent) + '  REC DSP Num:    %d\n' % self.recdspnum
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIHardwareStructVersionBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()
        ret.version           = megdata_read_int16(fd)
        ret.struct_size       = megdata_read_int16(fd)
        ret.entries           = megdata_read_int16(fd)
        os.lseek(fd, 8, os.SEEK_CUR)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIHardwareStructVersionBlock\n'
        s += (' ' * indent) + '  Version:        %d\n' % self.version
        s += (' ' * indent) + '  Struct Size:    %d\n' % self.struct_size
        s += (' ' * indent) + '  Entries:        %d\n' % self.entries
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_WHChanMapVer'] = BTIHardwareStructVersionBlock
BTI_USERBLOCKS['B_WHSubsysVer']  = BTIHardwareStructVersionBlock

class BTIChannelMapBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        # Need to find the number of channels from B_WHChanMapVer
        num_channels = None
        for block in blocks:
            if block.hdr.blocktype == 'B_WHChanMapVer':
                num_channels = block.data.entries
                break

        if num_channels is None:
            raise ValueError("Cannot find B_WHChanMapVer to determine number of channels")

        ret = cls()
        ret.channels = []
        for c in range(num_channels):
            ch = BTIChanConfig.from_fd(fd)
            ret.channels.append(ch)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIChannelMapBlock\n'
        for c in self.channels:
            s += c.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_WHChanMap'] = BTIChannelMapBlock

class BTIHardwareSubsysConfig(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.subsys_type       = megdata_read_int16(fd)
        ret.subsys_num        = megdata_read_int16(fd)
        ret.cards_per_sys     = megdata_read_int16(fd)
        ret.channels_per_card = megdata_read_int16(fd)
        ret.card_version      = megdata_read_int16(fd)
        # Structure padding
        os.lseek(fd, 2, os.SEEK_CUR)
        ret.offsetdacgain     = megdata_read_float(fd)
        ret.squid_type        = megdata_read_int32(fd)
        ret.timesliceoffset   = megdata_read_int16(fd)
        ret.padding           = megdata_read_int16(fd)
        ret.volts_per_bit     = megdata_read_float(fd)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIHardwareSubsysConfig\n'
        s += (' ' * indent) + '  Subsys Type:    %d\n' % self.subsys_type
        s += (' ' * indent) + '  Subsys Num:     %d\n' % self.subsys_num
        s += (' ' * indent) + '  Cards Per Sys:  %d\n' % self.cards_per_sys
        s += (' ' * indent) + '  Chans Per Card: %d\n' % self.channels_per_card
        s += (' ' * indent) + '  Card Version:   %d\n' % self.card_version
        s += (' ' * indent) + '  Offset DAC Gain:%e\n' % self.offsetdacgain
        s += (' ' * indent) + '  SQUID Type:     %d\n' % self.squid_type
        s += (' ' * indent) + '  Time Slice Off: %d\n' % self.timesliceoffset
        s += (' ' * indent) + '  Volts Per Bit:  %e\n' % self.volts_per_bit
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTISubsysMapBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        # Need to find the number of channels from B_WHSubsysVer
        num_subsys = None
        for block in blocks:
            if block.hdr.blocktype == 'B_WHSubsysVer':
                num_subsys = block.data.entries
                break

        if num_subsys is None:
            raise ValueError("Cannot find B_WHSubsysVer to determine number of subsystems")

        ret = cls()
        ret.subsys = []
        for s in range(num_subsys):
            su = BTIHardwareSubsysConfig.from_fd(fd)
            ret.subsys.append(su)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTISubsysMapBlock\n'
        for ss in self.subsys:
            s += ss.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_WHSubsys'] = BTISubsysMapBlock

#############################################################################
# Channel label block
#############################################################################

class BTIChannelLabelBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        ret.version        = megdata_read_int32(fd)
        ret.entries        = megdata_read_int32(fd)
        # Skip some int32 padding
        os.lseek(fd, 16, os.SEEK_CUR)

        # Read the labels
        ret.labels         = []

        for l in range(ret.entries):
            lb = megdata_read_str(fd, 16)
            ret.labels.append( lb )

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIChannelLabelBlock\n'
        s += (' ' * indent) + '  Version:        %d\n' % self.version
        s += (' ' * indent) + '  Entries:        %d\n' % self.entries

        for l in range(len(self.labels)):
            s += (' ' * indent) + '  Label %.3d:     %s\n' % (l, self.labels[l])
        s += (' ' * indent) + '>\n'

        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_ch_labels'] = BTIChannelLabelBlock

#############################################################################
# Calibration info block
#############################################################################

class BTICalibrationBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        ret.sensor_no      = megdata_read_int16(fd)
        # Structure padding
        os.lseek(fd, 2, os.SEEK_CUR)
        ret.timestamp      = megdata_read_int32(fd)
        ret.logdir         = megdata_read_str(fd, 256)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTICalibrationBlock\n'
        s += (' ' * indent) + '  Sensor num:       %d\n' % self.sensor_no
        s += (' ' * indent) + '  Timestamp:        %s (%d)\n' % (time.ctime(self.timestamp), self.timestamp)
        s += (' ' * indent) + '  Log Directory:    %s\n' % self.logdir
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_Calibration'] = BTICalibrationBlock

#############################################################################
# System configuration time block
#############################################################################

class BTISysConfigTimeBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        # XXX: This is wrong
        # We cannot hardcode the size of this string as it seems to vary across
        # platforms and config file version
        ret.sysconfig_name = megdata_read_str(fd, 512)
        ret.timestamp      = megdata_read_int32(fd)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTISysConfigTimeBlock\n'
        s += (' ' * indent) + '  Sensor num:       %s\n' % self.sysconfig_name
        s += (' ' * indent) + '  Timestamp:        %s (%d)\n' % (time.ctime(self.timestamp), self.timestamp)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

# This user block handler is disabled until the issue above
# is rectified.  The generic handler will be used instead.
# Most users do not need access to this block.
#BTI_USERBLOCKS['B_SysConfigTime'] = BTISysConfigTimeBlock

#############################################################################
# Delta enabled block
#############################################################################

class BTIDeltaEnabledBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        ret.delta_enabled  = megdata_read_int16(fd)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIDeltaEnabledBlock\n'
        s += (' ' * indent) + '  Delta Enabled:    %d\n' % self.delta_enabled
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_DELTA_ENABLED'] = BTIDeltaEnabledBlock

#############################################################################
# E-Table block
#############################################################################

class BTIETableHeader(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.version        = megdata_read_int32(fd)
        ret.entry_size     = megdata_read_int32(fd)
        ret.num_entries    = megdata_read_int32(fd)
        ret.filtername     = megdata_read_str(fd, 16)
        ret.num_E_values   = megdata_read_int32(fd)
        ret.reserved       = megdata_read_str(fd, 28)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIETableHeader\n'
        s += (' ' * indent) + '  Version:          %d\n' % self.version
        s += (' ' * indent) + '  Entry Size:       %d\n' % self.entry_size
        s += (' ' * indent) + '  Num entries:      %d\n' % self.num_entries
        s += (' ' * indent) + '  Filtername:       %s\n' % self.filtername
        s += (' ' * indent) + '  Num E values:     %d\n' % self.num_E_values
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIETableBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        ret.hdr            = BTIETableHeader.from_fd(fd)

        if ret.hdr.version == 2:
            ret.chan_names     = []
            for e in range(ret.hdr.num_entries):
                val = megdata_read_str(fd, 16)
                ret.chan_names.append( val )

            ret.e_chan_names   = []
            for e in range(ret.hdr.num_E_values):
                val = megdata_read_str(fd, 16)
                ret.e_chan_names.append( val )

            ret.etable = megdata_read_float_matrix(fd, ret.hdr.num_entries, ret.hdr.num_E_values)

        else:
            # Fixed style WH2500 format - channel names aren't stored but must
            # match CFO block of config file
            ret.chan_names = ['WH2500'] * ret.hdr.num_entries
            ret.hdr.num_E_values = 6
            ret.e_chan_names = ['MxA', 'MyA', 'MzA', 'MxaA', 'MyaA', 'MzaA']
            ret.etable = megdata_read_float_matrix(fd, ret.hdr.num_entries, ret.hdr.num_E_values)

            # Deal with padding
            curpos = os.lseek(fd, 0, os.SEEK_CUR);
            if ((curpos % 8) != 0):
                os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)


        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIETableBlock\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += (' ' * indent) + '  Channel Names:\n'
        for ch in self.chan_names:
            s += (' ' * indent) + '    %s\n' % ch
        s += (' ' * indent) + '  E-Channel Names:\n'
        for ch in self.e_chan_names:
            s += (' ' * indent) + '    %s\n' % ch
        s += (' ' * indent) + '  E-Table:        ' + megdata_array_print(self.etable, indent+18) + '\n'
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_E_table_used'] = BTIETableBlock
BTI_USERBLOCKS['B_E_TABLE'] = BTIETableBlock

#############################################################################
# Weight Table block
#############################################################################

class BTIWeightTableHeader(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.version        = megdata_read_int32(fd)
        ret.entry_size     = megdata_read_int32(fd)
        ret.num_entries    = megdata_read_int32(fd)
        ret.name           = megdata_read_str(fd, 32)
        ret.description    = megdata_read_str(fd, 80)
        ret.num_analog     = megdata_read_int32(fd)
        ret.num_dsp        = megdata_read_int32(fd)
        ret.reserved       = megdata_read_str(fd, 72)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIWeightTableHeader\n'
        s += (' ' * indent) + '  Version:          %d\n' % self.version
        s += (' ' * indent) + '  Entry Size:       %d\n' % self.entry_size
        s += (' ' * indent) + '  Num entries:      %d\n' % self.num_entries
        s += (' ' * indent) + '  Name:             %s\n' % self.name
        s += (' ' * indent) + '  Description:      %s\n' % self.description
        s += (' ' * indent) + '  Num Analog:       %d\n' % self.num_analog
        s += (' ' * indent) + '  Num DSP:          %d\n' % self.num_dsp
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIWeightTableBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        ret.hdr            = BTIWeightTableHeader.from_fd(fd)

        if ret.hdr.version == 2:
            ret.chan_names     = []
            for e in range(ret.hdr.num_entries):
                val = megdata_read_str(fd, 16)
                ret.chan_names.append( val )

            ret.analog_chan_names = []
            for e in range(ret.hdr.num_analog):
                val = megdata_read_str(fd, 16)
                ret.analog_chan_names.append( val )

            ret.dsp_chan_names = []
            for e in range(ret.hdr.num_dsp):
                val = megdata_read_str(fd, 16)
                ret.dsp_chan_names.append( val )

            ret.dsp_wts = megdata_read_float_matrix(fd, ret.hdr.num_entries, ret.hdr.num_dsp)

            ret.analog_wts = megdata_read_int16_matrix(fd, ret.hdr.num_entries, ret.hdr.num_analog)

        else:
            # Fixed style WH2500 format - channel names aren't stored but must
            # match CFO block of config file
            ret.chan_names = ['WH2500'] * ret.hdr.num_entries
            ret.analog_chan_names = ['MxA', 'MyA', 'MzA']
            ret.hdr.num_analog = len(ret.analog_chan_names)
            ret.dsp_chan_names = ['MxA', 'MyA', 'MzA', 'MxaA', 'MyaA', 'MzaA', 'GxxA', 'GyyA', 'GyxA', 'GzaA', 'GzyA']
            ret.hdr.num_dsp = len(ret.dsp_chan_names)

            ret.analog_wts = zeros( (ret.hdr.num_entries, ret.hdr.num_analog), dtype=int16 )
            ret.dsp_wts = zeros( (ret.hdr.num_entries, ret.hdr.num_dsp), dtype=float )
            for w in range(ret.hdr.num_entries):
                ret.analog_wts[w, :] = megdata_read_int16_matrix(fd, 1, ret.hdr.num_analog)
                # Skip an int16
                megdata_read_int16(fd)
                ret.dsp_wts[w, :] = megdata_read_float_matrix(fd, 1, ret.hdr.num_dsp)

            # Deal with padding
            curpos = os.lseek(fd, 0, os.SEEK_CUR)
            if ((curpos % 8) != 0):
                os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)



        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIWeightTableBlock\n'
        s += self.hdr.str_indent(indent=indent+2)


        s += (' ' * indent) + '  Channel Names:\n'
        for ch in self.chan_names:
            s += (' ' * indent) + '    %s\n' % ch

        s += (' ' * indent) + '  Analog Channel Names:\n'
        for ch in self.analog_chan_names:
            s += (' ' * indent) + '    %s\n' % ch
        s += (' ' * indent) + '  Analog Weights: ' + megdata_array_print(self.analog_wts, indent+18) + '\n'

        s += (' ' * indent) + '  DSP Channel Names:\n'
        for ch in self.dsp_chan_names:
            s += (' ' * indent) + '    %s\n' % ch
        s += (' ' * indent) + '  DSP Weights:    ' + megdata_array_print(self.dsp_wts, indent+18) + '\n'

        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_weights_used'] = BTIWeightTableBlock

#############################################################################
# TrigMask structures
#############################################################################

class BTITrigMaskEntry(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.name          = megdata_read_str(fd, 20)
        ret.nbits         = megdata_read_uint16(fd)
        ret.shift         = megdata_read_uint16(fd)
        ret.mask          = megdata_read_uint32(fd)
        # Structure padding
        os.lseek(fd, 8, os.SEEK_CUR)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTITrigMaskEntry\n'
        s += (' ' * indent) + '  Name:           %s\n' % self.name
        s += (' ' * indent) + '  NBits:          %d\n' % self.nbits
        s += (' ' * indent) + '  Shift:          %d\n' % self.shift
        s += (' ' * indent) + '  Mask:           0x%.8x\n' % self.mask
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTITrigMaskBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        ret.version         = megdata_read_int32(fd)
        ret.entries         = megdata_read_int32(fd)
        # Structure padding
        os.lseek(fd, 16, os.SEEK_CUR)

        ret.masks           = []

        for e in range(ret.entries):
            m = BTITrigMaskEntry.from_fd(fd)
            ret.masks.append(m)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTITrigMaskBlock\n'
        s += (' ' * indent) + '  Version:        %s\n' % self.version
        s += (' ' * indent) + '  Entries:        %s\n' % self.entries
        for m in self.masks:
            s += m.str_indent(indent=indent + 2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

BTI_USERBLOCKS['B_trig_mask'] = BTITrigMaskBlock

#############################################################################
# Unknown User block fake class
#############################################################################
class BTIUnknownUserBlock(object):
    def __init__(self, data):
        self.data = data

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIUnknownUserBlock>\n'
        return s

    def __str__(self):
        return self.str_indent()

#############################################################################
# User block header
#############################################################################
class BTIUserBlockHeader(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ## Process Header
        ret.nbytes          = megdata_read_int32(fd)
        ret.blocktype       = megdata_read_str(fd, 20)
        ret.checksum        = megdata_read_int32(fd)

        ## Remaining parts of block header
        ret.username        = megdata_read_str(fd, 32)
        ret.timestamp       = megdata_read_int32(fd)
        ret.user_space_size = megdata_read_int32(fd)
        ret.reserved        = megdata_read_char(fd, 32)

        # Deal with padding
        curpos = os.lseek(fd, 0, os.SEEK_CUR);
        if ((curpos % 8) != 0):
            os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIUserBlockHeader\n'
        s +=  (' ' * indent) + '  NBytes:           %d\n' % self.nbytes
        s +=  (' ' * indent) + '  BlockType:        %s\n' % self.blocktype
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '  Username:         %s\n' % self.username
        s +=  (' ' * indent) + '  Timestamp:        %s (%d)\n' % (time.ctime(self.timestamp), self.timestamp)
        s +=  (' ' * indent) + '  User Space Size:  %d\n' % self.user_space_size
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

#############################################################################
# User block wrapper class
#############################################################################
class BTIUserBlock(object):
    @classmethod
    def from_fd(cls, fd, blocks=None):
        ret = cls()

        # Block header
        ret.hdr = BTIUserBlockHeader.from_fd(fd)

        if ret.hdr.blocktype in list(BTI_USERBLOCKS.keys()):
            ret.data = BTI_USERBLOCKS[ret.hdr.blocktype].from_fd(fd, blocks)
        elif ret.hdr.blocktype.startswith('BWT_'):
            # Special case for weight tables in the system config file
            ret.data = BTIWeightTableBlock.from_fd(fd, blocks)
        else:
            # As we don't understand the type, just read the data as a blob
            data            = megdata_read_char(fd, ret.hdr.user_space_size)
            # And then stick it in a fake object
            ret.data = BTIUnknownUserBlock(data)

        # Deal with padding
        curpos = os.lseek(fd, 0, os.SEEK_CUR);
        if ((curpos % 8) != 0):
            os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIUserBlock\n'
        s += self.hdr.str_indent(indent=indent+2)
        s += self.data.str_indent(indent=indent+2)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

