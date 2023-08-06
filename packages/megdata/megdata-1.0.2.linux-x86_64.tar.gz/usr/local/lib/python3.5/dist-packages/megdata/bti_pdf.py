import os
import time
import numpy

from .common import *
from .bti_process import *

BTI_DATATYPE_SHORT  = 1
BTI_DATATYPE_LONG   = 2
BTI_DATATYPE_FLOAT  = 3
BTI_DATATYPE_DOUBLE = 4

BTI_NUMPY_DATATYPES = {BTI_DATATYPE_SHORT:  numpy.dtype('>i2'),
                       BTI_DATATYPE_LONG:   numpy.dtype('>i4'),
                       BTI_DATATYPE_FLOAT:  numpy.dtype('>f4'),
                       BTI_DATATYPE_DOUBLE: numpy.dtype('>f8')}

class BTIPDFHeaderData(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.version            = megdata_read_int16(fd)
        ret.file_type          = megdata_read_str(fd, 5)
        # Structure padding
        os.lseek(fd, 1, os.SEEK_CUR)
        ret.data_format        = megdata_read_int16(fd)
        ret.acq_mode           = megdata_read_int16(fd)
        ret.total_epochs       = megdata_read_int32(fd)
        ret.input_epochs       = megdata_read_int32(fd)
        ret.total_events       = megdata_read_int32(fd)
        ret.total_fixed_events = megdata_read_int32(fd)
        ret.sample_period      = megdata_read_float(fd)
        ret.xaxis_label        = megdata_read_str(fd, 16)
        ret.total_processes    = megdata_read_int32(fd)
        ret.total_chans        = megdata_read_int16(fd)
        # Structure padding
        os.lseek(fd, 2, os.SEEK_CUR)
        ret.checksum           = megdata_read_int32(fd)
        ret.total_ed_classes   = megdata_read_int32(fd)
        ret.total_associated_files = megdata_read_int16(fd)
        ret.last_file_index    = megdata_read_int16(fd)
        ret.timestamp          = megdata_read_int32(fd)
        # Structure padding
        os.lseek(fd, 20, os.SEEK_CUR)

        # Deal with padding
        curpos = os.lseek(fd, 0, os.SEEK_CUR);
        if ((curpos % 8) != 0):
            os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIPDFHeaderData\n'
        s +=  (' ' * indent) + '  Version:          %d\n' % self.version
        s +=  (' ' * indent) + '  File Type:        %s\n' % self.file_type
        s +=  (' ' * indent) + '  Data Format:      %d\n' % self.data_format
        s +=  (' ' * indent) + '  Acq Mode:         %d\n' % self.acq_mode
        s +=  (' ' * indent) + '  Total Epochs:     %d\n' % self.total_epochs
        s +=  (' ' * indent) + '  Input Epochs:     %d\n' % self.input_epochs
        s +=  (' ' * indent) + '  Total Events:     %d\n' % self.total_events
        s +=  (' ' * indent) + '  Total Fix Events: %d\n' % self.total_fixed_events
        s +=  (' ' * indent) + '  Sample Period:    %f\n' % self.sample_period
        s +=  (' ' * indent) + '  X-Axis Label:     %s\n' % self.xaxis_label
        s +=  (' ' * indent) + '  Total Processes:  %d\n' % self.total_processes
        s +=  (' ' * indent) + '  Total Chans:      %d\n' % self.total_chans
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '  Total Ed Classes: %d\n' % self.total_ed_classes
        s +=  (' ' * indent) + '  Total Assc Files: %d\n' % self.total_associated_files
        s +=  (' ' * indent) + '  Last File Index:  %d\n' % self.last_file_index
        s +=  (' ' * indent) + '  Timestamp:        %s (%d)\n' % (time.ctime(self.timestamp), self.timestamp)
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIPDFEpoch(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.pts_in_epoch       = megdata_read_int32(fd)
        ret.epoch_duration     = megdata_read_float(fd)
        ret.expected_iti       = megdata_read_float(fd)
        ret.actual_iti         = megdata_read_float(fd)
        ret.total_var_events   = megdata_read_int32(fd)
        ret.checksum           = megdata_read_int32(fd)
        ret.epoch_timestamp    = megdata_read_int32(fd)

        # Structure padding
        os.lseek(fd, 28, os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIPDFEpoch\n'
        s +=  (' ' * indent) + '  Pts in Epoch:     %d\n' % self.pts_in_epoch
        s +=  (' ' * indent) + '  Epoch Duration:   %f\n' % self.epoch_duration
        s +=  (' ' * indent) + '  Expected ITI:     %f\n' % self.expected_iti
        s +=  (' ' * indent) + '  Actual ITI:       %f\n' % self.actual_iti
        s +=  (' ' * indent) + '  Total Var Events: %d\n' % self.total_var_events
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '  Epoch Timestamp:  %d\n' % self.epoch_timestamp
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIPDFChannel(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.chan_label         = megdata_read_str(fd, 16)
        ret.chan_no            = megdata_read_int16(fd)
        ret.attributes         = megdata_read_int16(fd)
        ret.scale              = megdata_read_float(fd)
        ret.yaxis_label        = megdata_read_str(fd, 16)
        ret.valid_min_max      = megdata_read_int16(fd)
        # Structure padding
        os.lseek(fd, 6, os.SEEK_CUR)
        ret.ymin               = megdata_read_double(fd)
        ret.ymax               = megdata_read_double(fd)
        ret.index              = megdata_read_int32(fd)
        ret.checksum           = megdata_read_int32(fd)
        ret.off_flag           = megdata_read_str(fd, 16)
        ret.offset             = megdata_read_float(fd)
        # Structure padding
        os.lseek(fd, 12, os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIPDFChannel\n'
        s +=  (' ' * indent) + '  Channel Label:    %s\n' % self.chan_label
        s +=  (' ' * indent) + '  Channel No:       %d\n' % self.chan_no
        s +=  (' ' * indent) + '  Attributes:       %d\n' % self.attributes
        s +=  (' ' * indent) + '  Scale:            %f\n' % self.scale
        s +=  (' ' * indent) + '  Y-Axis Label:     %s\n' % self.yaxis_label
        s +=  (' ' * indent) + '  Valid Min/Max:    %d\n' % self.valid_min_max
        s +=  (' ' * indent) + '  YMin:             %e\n' % self.ymin
        s +=  (' ' * indent) + '  YMax:             %e\n' % self.ymax
        s +=  (' ' * indent) + '  Index:            %d\n' % self.index
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '  Off Flag:         %s\n' % self.off_flag
        s +=  (' ' * indent) + '  Offset:           %e\n' % self.offset
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIPDFEvent(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.event_name         = megdata_read_str(fd, 16)
        ret.start_lat          = megdata_read_float(fd)
        ret.end_lat            = megdata_read_float(fd)
        ret.step_size          = megdata_read_float(fd)
        ret.fixed_event        = megdata_read_int16(fd)
        ret.checksum           = megdata_read_int32(fd)
        # Structure padding
        os.lseek(fd, 32, os.SEEK_CUR)

        # Deal with padding
        curpos = os.lseek(fd, 0, os.SEEK_CUR);
        if ((curpos % 8) != 0):
            os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIPDFEvent\n'
        s +=  (' ' * indent) + '  Event Name:       %s\n' % self.event_name
        s +=  (' ' * indent) + '  Start Latency:    %f\n' % self.start_lat
        s +=  (' ' * indent) + '  End Latency:      %f\n' % self.end_lat
        s +=  (' ' * indent) + '  Step Size:        %f\n' % self.step_size
        s +=  (' ' * indent) + '  Fixed Event:      %d\n' % self.fixed_event
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIPDFProcess(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        # Process header
        ret.nbytes             = megdata_read_int32(fd)
        ret.blocktype          = megdata_read_str(fd, 20)
        ret.checksum           = megdata_read_int32(fd)

        # Rest of it
        ret.user               = megdata_read_str(fd, 32)
        ret.timestamp          = megdata_read_int32(fd)
        ret.filename           = megdata_read_str(fd, 256)
        ret.total_steps        = megdata_read_int32(fd)

        # Structure padding
        os.lseek(fd, 32, os.SEEK_CUR)

        # Deal with padding
        curpos = os.lseek(fd, 0, os.SEEK_CUR);
        if ((curpos % 8) != 0):
            os.lseek(fd, (8 - (curpos % 8)), os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIPDFProcess\n'
        s +=  (' ' * indent) + '  NBytes:           %d\n' % self.nbytes
        s +=  (' ' * indent) + '  BlockType:        %s\n' % self.blocktype
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '  User:             %s\n' % self.user
        s +=  (' ' * indent) + '  Timestamp:        %s (%d)\n' % (time.ctime(self.timestamp), self.timestamp)
        s +=  (' ' * indent) + '  Filename:         %s\n' % self.filename
        s +=  (' ' * indent) + '  Total Steps:      %d\n' % self.total_steps
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIPDFAssocFile(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.file_id            = megdata_read_int16(fd)
        ret.length             = megdata_read_int16(fd)
        # Structure padding
        os.lseek(fd, 32, os.SEEK_CUR)
        ret.checksum           = megdata_read_int32(fd)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIPDFAssocFile\n'
        s +=  (' ' * indent) + '  File ID:          %d\n' % self.file_id
        s +=  (' ' * indent) + '  Length:           %d\n' % self.length
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIPDFEdClass(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.comment_size       = megdata_read_int32(fd)
        ret.name               = megdata_read_str(fd, 17)
        # Structure padding
        os.lseek(fd, 9, os.SEEK_CUR)
        ret.pdf_number         = megdata_read_int16(fd)
        ret.total_events       = megdata_read_int32(fd)
        ret.timestamp          = megdata_read_int32(fd)
        ret.flags              = megdata_read_int32(fd)
        ret.de_process         = megdata_read_int32(fd)
        ret.checksum           = megdata_read_int32(fd)
        ret.ed_id              = megdata_read_int32(fd)
        ret.win_width          = megdata_read_float(fd)
        ret.win_offset         = megdata_read_float(fd)
        # Structure padding
        os.lseek(fd, 8, os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIPDFEdClass\n'
        s +=  (' ' * indent) + '  Comment Size:     %d\n' % self.comment_size
        s +=  (' ' * indent) + '  Name:             %s\n' % self.name
        s +=  (' ' * indent) + '  PDF Number:       %d\n' % self.pdf_number
        s +=  (' ' * indent) + '  Total Events:     %d\n' % self.total_events
        s +=  (' ' * indent) + '  Timestamp:        %d\n' % self.timestamp
        s +=  (' ' * indent) + '  Flags:            %d\n' % self.flags
        s +=  (' ' * indent) + '  DE Process:       %d\n' % self.de_process
        s +=  (' ' * indent) + '  Checksum:         %d\n' % self.checksum
        s +=  (' ' * indent) + '  ID:               %d\n' % self.ed_id
        s +=  (' ' * indent) + '  Win Width:        %f\n' % self.win_width
        s +=  (' ' * indent) + '  Win Offset:       %f\n' % self.win_offset
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIPDF(object):
    @classmethod
    def from_file(cls, filename):
        """
        Read a BTI-style data file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        # Seek to the end of the file minus 8 bytes
        ftr_pos = os.lseek(fd, -8, os.SEEK_END)

        # Now read the last 8 bytes
        hdr_pos = megdata_read_int64(fd)
        mask = 2147483647
        test_val = hdr_pos & mask

        if ((ftr_pos + 8 - test_val) <= 2147483647):
            hdr_pos = test_val

        # Check for alignment issues
        if ((hdr_pos % 8) != 0):
            hdr_pos += (8 - (hdr_pos % 8))

        # Finally seek to the start of the header
        os.lseek(fd, hdr_pos, os.SEEK_SET)

        # Figure out the header size
        hdr_size = ftr_pos - hdr_pos

        ret.hdr = BTIPDFHeaderData.from_fd(fd)

        ret.epochs = []
        for e in range(ret.hdr.total_epochs):
            ep = BTIPDFEpoch.from_fd(fd)
            ret.epochs.append( ep )

        ret.channels = []
        for c in range(ret.hdr.total_chans):
            ch = BTIPDFChannel.from_fd(fd)
            ret.channels.append( ch )

        ret.events = []
        for e in range(ret.hdr.total_events):
            ev = BTIPDFEvent.from_fd(fd)
            ret.events.append( ev )

        ret.processes = []
        for p in range(ret.hdr.total_processes):
            pr = BTIProcess.from_fd(fd)
            ret.processes.append( pr )

        ret.assocfiles = []
        for f in range(ret.hdr.total_associated_files):
            af = BTIPDFAssocFile.from_fd(fd)
            ret.assocfiles.append( af )

        ret.edclasses = []
        for e in range(ret.hdr.total_ed_classes):
            ec = BTIPDFEdClass.from_fd(fd)
            ret.edclasses.append( ec )

        # We load any remaining data
        curpos = os.lseek(fd, 0, os.SEEK_CUR)
        ret.extradata = os.read(fd, ftr_pos - curpos)

        # Stash a copy of the FD in case we need to load data later
        # We need to take our own copy so that if someone closes it
        # underneath us, bad things don't happen
        ret.fd = os.fdopen(os.dup(fd), 'r')

        return ret

    def str_indent(self, indent=0):
        s =  (' ' * indent) + '<BTIPDF\n'

        s += self.hdr.str_indent(indent=indent+2)

        s += (' ' * indent) + '  Epochs:\n'
        for e in self.epochs:
            s += e.str_indent(indent=indent+4)

        s += (' ' * indent) + '  Channels:\n'
        for c in self.channels:
            s += c.str_indent(indent=indent+4)

        s += (' ' * indent) + '  Events:\n'
        for e in self.events:
            s += e.str_indent(indent=indent+4)

        s += (' ' * indent) + '  Processes:\n'
        for p in self.processes:
            s += p.str_indent(indent=indent+4)

        s += (' ' * indent) + '  Associated Files:\n'
        for a in self.assocfiles:
            s += a.str_indent(indent=indent+4)

        s += (' ' * indent) + '  Ed Classes:\n'
        for e in self.edclasses:
            s += e.str_indent(indent=indent+4)

        if len(self.extradata) > 0:
            s += (' ' * indent) + '  Length of unknown data: %d\n' % len(self.extradata)

        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

    @property
    def total_slices(self):
        total_slices = 0
        for e in self.epochs:
            total_slices += e.pts_in_epoch
        return total_slices

    @property
    def numpy_datatype(self):
        return BTI_NUMPY_DATATYPES[self.hdr.data_format]

    @property
    def bytes_per_slice(self):
        return self.numpy_datatype.itemsize * self.hdr.total_chans

    def read_raw_data(self, slices=None, indices=None):
        total_slices = self.total_slices
        # If slices is None, return all data
        if slices is None:
            startp = 0
            endp = total_slices
        else:
            startp = slices[0]
            endp = slices[1]

        if (startp < 0) or (endp > total_slices) or (startp >= endp):
            raise RuntimeError('Invalid start and end slices for get_slice_range(): %d, %d' % (startp, endp))

        self.fd.seek(self.bytes_per_slice * startp)

        unordered_data = numpy.reshape(numpy.fromfile(self.fd,
                                                      dtype = self.numpy_datatype, \
                                                      count = (endp - startp) * self.hdr.total_chans), \
                                                      [endp - startp, self.hdr.total_chans])

        if indices is None:
            # Return everything unordered
            data = unordered_data
        else:
            data = unordered_data[:, indices]

            del unordered_data

        return data

    def channel(self, chan_label):
        ret = None
        for e in self.channels:
            if e.chan_label == chan_label:
                # Check for multiple channels and raise an error
                if ret is not None:
                    raise Exception('Multiple channels with name %s found' % chan_label)
                ret = e
        return ret

    def find_first_event(self, eventname):
        for e in self.events:
            if e.event_name == eventname:
                return e
        return None

    def slice_to_latency(self, slicenum):
        trigev = self.find_first_event('Trigger')
        period = self.hdr.sample_period

        return (slicenum * period) - trigev.start_lat

    def latency_to_slice(self, latency):
        trigev = self.find_first_event('Trigger')
        period = self.hdr.sample_period

        ret = float(latency + trigev.start_lat) / float(period)

        # Round
        return numpy.floor(ret + 0.5)
