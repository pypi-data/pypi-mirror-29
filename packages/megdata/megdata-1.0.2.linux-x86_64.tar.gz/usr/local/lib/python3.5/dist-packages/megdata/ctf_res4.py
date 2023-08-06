import os

from .common import *

class CTFCoeffEntry(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.name               = megdata_read_str(fd, 32)

        ret.ctype              = megdata_read_int32(fd)

        # Padding
        os.lseek(fd, 4, os.SEEK_CUR)

        ret.num_coeffs         = megdata_read_int16(fd)

        ret.sensor_tgts        = []

        for j in range(50):
            ret.sensor_tgts.append( megdata_read_str(fd, 31) )

        ret.sensor_coeffs      = megdata_read_double_matrix(fd, 50, 1)

        return ret

    def str_indent(self, indent=0):
        s = ''
        s += (' ' * indent) + '<CTFCoeffEntry\n'
        s += (' ' * indent) + '  Name:              %s\n' % self.name
        s += (' ' * indent) + '  Coeff Type:        %d\n' % self.ctype
        s += (' ' * indent) + '  Num Coeffs:        %d\n' % self.num_coeffs
        for j in range(self.num_coeffs):
            s += (' ' * indent) + '    Channel: %.31s  Coeff: %e\n' % (self.sensor_tgts[j], self.sensor_coeffs[j, 0])
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class CTFCoil(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.position           = megdata_read_vec3(fd)

        # Padding
        os.lseek(fd, 8, os.SEEK_CUR)

        ret.orientation        = megdata_read_vec3(fd)

        # Padding
        os.lseek(fd, 8, os.SEEK_CUR)

        ret.num_turns          = megdata_read_int16(fd)

        # Padding
        os.lseek(fd, 6, os.SEEK_CUR)

        ret.area               = megdata_read_double(fd)

        return ret

    def str_indent(self, indent=0):
        s = ''
        s += (' ' * indent) + '<CTFCoil\n'
        s += (' ' * indent) + '  Position:          ' + megdata_array_print(self.position) + '\n'
        s += (' ' * indent) + '  Orientation:       ' + megdata_array_print(self.orientation) + '\n'
        s += (' ' * indent) + '  Number of Turns:   %d\n' % self.num_turns
        s += (' ' * indent) + '  Area:              %f\n' % self.area
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

CTF_CHAN_REF_MAG   = 0  # Magnetometer reference
CTF_CHAN_REF_GRAD1 = 1  # 1st order gradiometer reference
CTF_CHAN_REF_GRAD2 = 2  # 2nd order gradiometer reference
CTF_CHAN_REF_GRAD3 = 3  # 3rd order gradiometer reference
CTF_CHAN_MAG       = 4  # Magnetometer
CTF_CHAN_GRAD1     = 5  # 1st order gradiometer
CTF_CHAN_GRAD2     = 6  # 2nd order gradiometer
CTF_CHAN_GRAD3     = 7  # 3rd order gradiometer
CTF_CHAN_REF_EEG   = 8  # EEG Reference
CTF_CHAN_EEG       = 9  # EEG
CTF_CHAN_ADC       = 10 # ADC channel
CTF_CHAN_STIM      = 11 # Stimulus channel
CTF_CHAN_TIME      = 12 # Time reference
CTF_CHAN_POS       = 13 # Position reference
CTF_CHAN_DAC       = 14 # DAC reference
CTF_CHAN_OTHER     = 15 # Other reference
CTF_CHAN_VIRTUAL   = 16 # Virtual Channel
CTF_CHAN_SYSTIME   = 17 # System Time Reference

CTF_CHANTYPES = {CTF_CHAN_REF_MAG   : 'Magnetometer reference',
                 CTF_CHAN_REF_GRAD1 : '1st order gradiometer reference',
                 CTF_CHAN_REF_GRAD2 : '2nd order gradiometer reference',
                 CTF_CHAN_REF_GRAD3 : '3rd order gradiometer reference',
                 CTF_CHAN_MAG       : 'Magnetometer',
                 CTF_CHAN_GRAD1     : '1st order gradiometer',
                 CTF_CHAN_GRAD2     : '2nd order gradiometer',
                 CTF_CHAN_GRAD3     : '3rd order gradiometer',
                 CTF_CHAN_REF_EEG   : 'EEG Reference',
                 CTF_CHAN_EEG       : 'EEG',
                 CTF_CHAN_ADC       : 'ADC channel',
                 CTF_CHAN_STIM      : 'Stimulus channel',
                 CTF_CHAN_TIME      : 'Time reference',
                 CTF_CHAN_POS       : 'Position reference',
                 CTF_CHAN_DAC       : 'DAC reference',
                 CTF_CHAN_OTHER     : 'Other reference',
                 CTF_CHAN_VIRTUAL   : 'Virtual Channel',
                 CTF_CHAN_SYSTIME   : 'System Time Reference'}

CTF_COILSHAPE_CIRCULAR = 0
CTF_COILSHAPE_SQUARE   = 1

CTF_COILSHAPES = {CTF_COILSHAPE_CIRCULAR: 'Circular',
                  CTF_COILSHAPE_SQUARE:   'Square'}

class CTFChannel(object):
    @classmethod
    def from_fd(cls, fd, channame):
        ret = cls()

        ret.name               = channame

        # Strip off the -XXXX machine number
        ret.nicename           = channame.split('-')[0]

        # Channel type (see above)
        ret.ctype              = megdata_read_int16(fd)

        ret.origin_run_num     = megdata_read_int16(fd)

        # 0 == CIRCULAR; 1 = SQUARE
        ret.coil_shape         = megdata_read_int32(fd)

        ret.gain               = megdata_read_double(fd)
        ret.q_gain             = megdata_read_double(fd)
        ret.io_gain            = megdata_read_double(fd)
        ret.io_offset          = megdata_read_double(fd)
        ret.num_coils          = megdata_read_int16(fd)
        if ret.num_coils > 8:
            ret.num_coils = 8
        ret.grad_order_num     = megdata_read_int16(fd)

        # Structure padding
        os.lseek(fd, 4, os.SEEK_CUR)

        ret.coils = []
        for c in range(8):
            ret.coils.append( CTFCoil.from_fd(fd) )

        ret.hd_coils = []
        for c in range(8):
            ret.hd_coils.append( CTFCoil.from_fd(fd) )

        return ret

    def str_indent(self, indent=0):
        s = ''
        s += (' ' * indent) + '<CTFChannel\n'
        s += (' ' * indent) + '  Name:              %s\n' % self.name
        s += (' ' * indent) + '  Channel Type:      %d (%s)\n' % (self.ctype, CTF_CHANTYPES.get(self.ctype, 'UNKNOWN'))
        s += (' ' * indent) + '  Origin Run Num:    %d\n' % self.origin_run_num
        s += (' ' * indent) + '  Coil Shape:        %d\n' % self.coil_shape
        s += (' ' * indent) + '  Gain:              %e\n' % self.gain
        s += (' ' * indent) + '  Q Gain:            %e\n' % self.q_gain
        s += (' ' * indent) + '  IO Gain:           %e\n' % self.io_gain
        s += (' ' * indent) + '  IO Offset:         %e\n' % self.io_offset
        s += (' ' * indent) + '  Grad Order No:     %d\n' % self.grad_order_num
        s += (' ' * indent) + '  Num Coils:         %d\n' % self.num_coils
        for cn in range(self.num_coils):
            s += (' ' * (indent+2)) + '  Coil %d:\n' % cn
            s += self.coils[cn].str_indent(indent=indent+4)
            s += (' ' * (indent+2)) + '  Coil %d (HD):\n' % cn
            s += self.hd_coils[cn].str_indent(indent=indent+4)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class CTFFilter(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.frequency          = megdata_read_float(fd)
        # 0 == CLASSERROR; 1 == BUTTERWORTH
        ret.filter_class       = megdata_read_int32(fd)
        # 0 == TYPERROR; 1 == LOWPASS; 2 == HIGHPASS; 3 == NOTCH
        ret.filter_type        = megdata_read_int32(fd)
        ret.num_params         = megdata_read_int16(fd)
        ret.params             = megdata_read_float(fd, ret.num_params)

        return ret

    def str_indent(self, indent=0):
        s = ''
        s += (' ' * indent) + '<CTFFilter\n'
        s += (' ' * indent) + '  Frequency:         %f\n' % self.frequency
        s += (' ' * indent) + '  Filter Class:      %d\n' % self.filter_class
        s += (' ' * indent) + '  Filter Type:       %d\n' % self.filter_type
        s += (' ' * indent) + '  Num Params:        %d\n' % self.num_params
        s += (' ' * indent) + '  Parameters:        ' + megdata_array_print(self.params, indent=indent+2) + '\n'
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class CTFRes4File(object):
    @classmethod
    def from_file(cls, filename):
        """
        Read a CTF Res4 file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.version            = megdata_read_str(fd, 8)
        if ret.version != 'MEG41RS' and ret.version != 'MEG42RS':
            raise ValueError('Only support MEG41RS and MEG42RS versions at the moment (%s)' % ret.version)

        ret.app_name           = megdata_read_str(fd, 256)
        ret.data_origin        = megdata_read_str(fd, 256)
        ret.data_desc          = megdata_read_str(fd, 256)
        ret.no_trials_avg      = megdata_read_int16(fd)
        ret.data_time          = megdata_read_str(fd, 255)
        ret.data_date          = megdata_read_str(fd, 255)

        ret.no_samples         = megdata_read_int32(fd)
        ret.no_channels        = megdata_read_int16(fd)

        # Structure padding
        os.lseek(fd, 2, os.SEEK_CUR)

        ret.sample_rate        = megdata_read_double(fd)
        ret.epoch_time         = megdata_read_double(fd)
        ret.no_trials          = megdata_read_int16(fd)
        ret.no_trials_done     = megdata_read_int16(fd)
        ret.pre_trig_pts       = megdata_read_int32(fd)
        ret.no_trials_display  = megdata_read_int16(fd)
        ret.save_trials        = megdata_read_int8(fd)

        # Structure padding
        os.lseek(fd, 2, os.SEEK_CUR)

        ret.primary_trigger    = megdata_read_uint32(fd)
        ret.trig_pol_mask      = megdata_read_uint32(fd)
        ret.trigger_mode       = megdata_read_int16(fd)
        ret.accept_reject_flag = megdata_read_bool(fd)
        ret.run_time_display   = megdata_read_int16(fd)
        ret.zero_head_flag     = megdata_read_bool(fd)
        ret.artifact_mode      = megdata_read_bool(fd)

        # Structure padding
        os.lseek(fd, 20, os.SEEK_CUR)

        ret.run_name           = megdata_read_str(fd, 32)
        ret.run_title          = megdata_read_str(fd, 256)
        ret.instruments        = megdata_read_str(fd, 32)
        ret.collect_descrip    = megdata_read_str(fd, 32)
        ret.subject_id         = megdata_read_str(fd, 32)
        ret.operator           = megdata_read_str(fd, 32)
        ret.sensor_filename    = megdata_read_str(fd, 60)
        ret.rdlen              = megdata_read_int32(fd)

        # Structure padding
        os.lseek(fd, 4, os.SEEK_CUR)

        ret.run_description    = megdata_read_str(fd, ret.rdlen)
        ret.num_filters        = megdata_read_int16(fd)

        ret.filters = []
        for f in range(ret.num_filters):
            ret.filters.append( CTFFilter.from_fd(fd) )

        # We store the channel names in the CTFChannel objects as we create them
        chan_names = []
        for c in range(ret.no_channels):
            chan_names.append( megdata_read_str(fd, 32) )

        ret.channels = []
        for c in range(ret.no_channels):
            ret.channels.append( CTFChannel.from_fd(fd, chan_names[c]) )

        ret.num_coeffs         = megdata_read_int16(fd)

        ret.coeffs = []
        for c in range(ret.num_coeffs):
            ret.coeffs.append( CTFCoeffEntry.from_fd(fd) )

        return ret

    def str_indent(self, indent=0):
        s = ''
        s += (' ' * indent) + '<CTFRes4File\n'
        s += (' ' * indent) + '  Version:           %s\n' % self.version
        s += (' ' * indent) + '  App Name:          %s\n' % self.app_name
        s += (' ' * indent) + '  Data Origin:       %s\n' % self.data_origin
        s += (' ' * indent) + '  Data Description   %s\n' % self.data_desc
        s += (' ' * indent) + '  No Trials Avg:     %d\n' % self.no_trials_avg
        s += (' ' * indent) + '  Data Time:         %s\n' % self.data_time
        s += (' ' * indent) + '  Data Date          %s\n' % self.data_date
        s += (' ' * indent) + '  No Samples:        %d\n' % self.no_samples
        s += (' ' * indent) + '  No Channels:       %d\n' % self.no_channels
        s += (' ' * indent) + '  Sample Rate:       %f\n' % self.sample_rate
        s += (' ' * indent) + '  Epoch Time:        %f\n' % self.epoch_time
        s += (' ' * indent) + '  No Trials:         %d\n' % self.no_trials
        s += (' ' * indent) + '  No Trials Done:    %d\n' % self.no_trials_done
        s += (' ' * indent) + '  Pre Trigger Pts:   %d\n' % self.pre_trig_pts
        s += (' ' * indent) + '  No Trials Display: %d\n' % self.no_trials_display
        s += (' ' * indent) + '  Save Trials:       %d\n' % self.save_trials
        s += (' ' * indent) + '  Primary Trigger:   %d\n' % self.primary_trigger
        s += (' ' * indent) + '  Trig Pol Mask:     0x%.8x\n' % self.trig_pol_mask
        s += (' ' * indent) + '  Trigger Mode:      %d\n' % self.trigger_mode
        s += (' ' * indent) + '  Acc/Rej Flag:      %d\n' % self.accept_reject_flag
        s += (' ' * indent) + '  Run Time Display:  %d\n' % self.run_time_display
        s += (' ' * indent) + '  Zero Head Flag:    %d\n' % self.zero_head_flag
        s += (' ' * indent) + '  Artifact Mode:     %d\n' % self.artifact_mode
        s += (' ' * indent) + '  Run Name:          %s\n' % self.run_name
        s += (' ' * indent) + '  Run Title:         %s\n' % self.run_title
        s += (' ' * indent) + '  Instruments:       %s\n' % self.instruments
        s += (' ' * indent) + '  Collect Desc:      %s\n' % self.collect_descrip
        s += (' ' * indent) + '  Subject ID:        %s\n' % self.subject_id
        s += (' ' * indent) + '  Operator:          %s\n' % self.operator
        s += (' ' * indent) + '  Sensor Filename:   %s\n' % self.sensor_filename
        s += (' ' * indent) + '  RDLen:             %d\n' % self.rdlen
        s += (' ' * indent) + '  Run Description:   %s\n' % self.run_description
        s += (' ' * indent) + '  Num Filters:       %d\n' % self.num_filters

        for f in self.filters:
            s += f.str_indent(indent=indent+2)
        s += (' ' * indent) + '  Channel Names:\n'

        for c in self.channels:
            s += c.str_indent(indent=indent+2)

        s += (' ' * indent) + '  Num Coeffs         %d\n' % self.num_coeffs

        for c in self.coeffs:
            s += c.str_indent(indent=indent+2)

        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

