#!/usr/bin/python

import os

from .common import *

class BTIDipole(object):
    """Individual dipole object within a .dipole file"""
    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        ret.position    = megdata_read_vec3(fd)
        ret.orientation = megdata_read_vec3(fd)
        ret.correlation = megdata_read_float(fd)
        ret.goodness    = megdata_read_float(fd)
        ret.cx          = megdata_read_float(fd)
        ret.cy          = megdata_read_float(fd)
        ret.cz          = megdata_read_float(fd)
        ret.rms         = megdata_read_float(fd)
        ret.latency     = megdata_read_float(fd)
        ret.epoch       = megdata_read_int16(fd)
        ret.iterations  = megdata_read_int16(fd)
        ret.color       = megdata_read_int16(fd)
        ret.shape       = megdata_read_int16(fd)
        ret.label       = megdata_read_str(fd, 65)
        ret.scan        = megdata_read_str(fd, 11)
        ret.session     = megdata_read_str(fd, 16)
        ret.run         = megdata_read_str(fd, 3)
        ret.pdf_name    = megdata_read_str(fd, 73)
        ret.patient     = megdata_read_str(fd, 11)
        # There is a byte of padding here
        megdata_read_char(fd, 1)
        ret.avgChannelNoise   = megdata_read_float(fd)
        ret.channelListLen    = megdata_read_int16(fd)
        # There are two bytes of padding here
        megdata_read_char(fd, 2)

        # Now we have to deal with the channelList
        ret.channelList = ''.join(megdata_read_char(fd, ret.channelListLen)[:-1]).split(',')

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIDipole\n'
        s +=  (' ' * indent) + '  Position:         ' + str(self.position) + '\n'
        s +=  (' ' * indent) + '  Orientation:      ' + str(self.orientation) + '\n'
        s +=  (' ' * indent) + '  Correlation:      %e\n' % self.correlation
        s +=  (' ' * indent) + '  Confidence Area:  %e %e %e\n' % (self.cx, self.cy, self.cz)
        s +=  (' ' * indent) + '  RMS:              %e\n'   % self.rms
        s +=  (' ' * indent) + '  Latency:          %.6f\n' % self.latency
        s +=  (' ' * indent) + '  Epoch:            %d\n' % self.epoch
        s +=  (' ' * indent) + '  Num Iterations:   %d\n' % self.iterations
        s +=  (' ' * indent) + '  Colour / Shape:   %d / %d\n' % (self.color, self.shape)
        # Skip label, scan, session, run, pdf name, patient
        s +=  (' ' * indent) + '  Avg Chan Noise:   %e\n' % (self.avgChannelNoise)
        s +=  (' ' * indent) + '  Num Channels:     %d\n' % len(self.channelList)
        s +=  (' ' * indent) + '  Channels:         %s\n' % ','.join(self.channelList)
        s +=  (' ' * indent) + '>\n'

        return s

    def __str__(self):
        return self.str_indent()


class BTIDipoleFile(object):
    @staticmethod
    def _parse_string(val):
        try:
            ret = val.split(' : ')[1]
            if ret.endswith(';'):
                ret = ret[:-1]
        except Exception as e:
            print(e)
            raise ValueError("Parse error reading string")

        return ret

    @classmethod
    def from_file(cls, filename):
        """
        Read a BTI dipole data file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()

        # The first three lines of the file and the rest are binary.  Urgh
        ret.version = ret._parse_string(megdata_read_bytes(fd))

        if ret.version != '4.0':
            raise Exception('Bad version number (only 4.0 supported)')

        # Split out the data
        ret.patient_id = ret._parse_string(megdata_read_bytes(fd))
        num_entries = int(ret._parse_string(megdata_read_bytes(fd)))

        ret.dipoles = []

        # Now read the dipoles
        # Each dipole is a BTIDipole entry followed by a channel list
        for k in range(num_entries):
            dip = BTIDipole.from_fd(fd)
            ret.dipoles.append(dip)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIDipoleFile\n'
        s +=  (' ' * indent) + '  Version:          %s\n' % self.version
        s +=  (' ' * indent) + '  Patient ID:       %s\n' % self.patient_id
        s +=  (' ' * indent) + '  Dipole Count:     %d\n' % len(self.dipoles)
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()


class BTIDipoleTextFile(object):
    @classmethod
    def from_file(cls, filename):
        """
        Read a BTI text dipole file from a filename
        """
        from numpy import array

        f = open(filename, 'r')
        ret = cls()
        ret.dipoles = []

        # Read all of the data in one go and then parse line-by-line
        data = [x.strip() for x in f.readlines()]

        cur_epoch = None
        average_noise = None

        patient = None
        scan = None
        session = None
        run = None
        pdf_name = None
        channel_group = None
        local_sphere = None
        ignored_chans = None

        # Lines to skip if they start with this
        skipif = ['Page', 'Output', 'Sensors', 'Default', 'Grid',
                  'Ignored', 'Patient', 'Latency', 'skipping', '(msec)']

        for line in data:
            skip = False

            # Skip known bad lines
            for s in skipif:
                if line.startswith(s):
                    skip = True

            # Skip blank lines
            if len(line.strip()) == 0:
                skip = True

            if skip:
                continue

            # Update our epoch number if necessary
            if line.startswith('EPOCH'):
                cur_epoch = int(line.split()[1])
                continue

            # Parse our average noise if necessary
            if line.startswith('Average Noise'):
                average_noise = float(line.split()[2])
                continue

            # Input information
            if line.startswith('Input'):
                line = line.split()
                patient = line[1]
                scan = line[2]
                session = ' '.join(line[3:5])
                run = int(line[5])
                pdf_name = line[6]
                channel_group = line[7]
                local_sphere = [float(x) for x in line[8].strip('(').strip(')').split(',')]
                continue

            if line.startswith('Ignored'):
                line = line.split()
                print(line)
                ignored_chans = line[3]
                continue

            # Try and parse the line
            linedat = line.split()

            # Should be 17 columns
            if len(linedat) != 17:
                print("Error, ", len(linedat))
                print(linedat)

            latency = float(linedat[0])
            # These need to be in m rather than cm
            x = float(linedat[1]) / 100.0
            y = float(linedat[2]) / 100.0
            z = float(linedat[3]) / 100.0
            Qx = float(linedat[4]) / 100.0
            Qy = float(linedat[5]) / 100.0
            Qz = float(linedat[6]) / 100.0
            radius = float(linedat[7]) / 100.0
            modQ = float(linedat[8])
            rms = float(linedat[9])
            # TODO: Work out units for this
            cvol = float(linedat[10])

            cx = float(linedat[11]) / 100.0
            cy = float(linedat[12]) / 100.0
            cz = float(linedat[13]) / 100.0
            corr = float(linedat[14])
            gof = float(linedat[15])
            iteration = int(linedat[16])

            # Create a BTIDipole object
            dip = BTIDipole()
            dip.position = array([[x, y, z]])
            dip.orientation = array([Qx, Qy, Qz])
            dip.correlation = corr
            dip.goodness = gof
            dip.cx = cx
            dip.cy = cy
            dip.cz = cz
            dip.rms = rms
            dip.latency = latency
            dip.epoch = cur_epoch
            dip.iterations = iteration

            # Hardcode these as 0 as there's no data in the file
            dip.color = 0
            dip.shape = 0
            dip.label = ''

            dip.scan = scan
            dip.session = session
            dip.run = run
            dip.pdf_name = pdf_name
            dip.patient = patient

            dip.avgChannelNoise = average_noise

            # Just store this as a single string for now
            dip.channelListLen = 1
            dip.channelList = [channel_group]

            ret.dipoles.append(dip)

        return ret

    def str_indent(self, indent=0):
        s =   (' ' * indent) + '<BTIDipoleTextFile\n'
        s +=  (' ' * indent) + '  Dipole Count:     %d\n' % len(self.dipoles)
        s +=  (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

