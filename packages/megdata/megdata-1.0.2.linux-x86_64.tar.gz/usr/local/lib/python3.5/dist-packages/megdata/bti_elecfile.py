import os
import struct

from .common import *

BTI_ELEC_STATE_NOT_COLLECTED  = 0
BTI_ELEC_STATE_COLLECTED      = 1
BTI_ELEC_STATE_SKIPPED        = 2
BTI_ELEC_STATE_NOT_APPLICABLE = 3

BTI_ELEC_STATES = {
        BTI_ELEC_STATE_NOT_COLLECTED:  "Not Collected",
        BTI_ELEC_STATE_COLLECTED:      "Collected",
        BTI_ELEC_STATE_SKIPPED:        "Skipped",
        BTI_ELEC_STATE_NOT_APPLICABLE: "Not Applicable"
}

class BTIElectrode(object):
    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.loc             = megdata_read_vec3(fd)
        ret.lbl             = megdata_read_str(fd, 16)
        ret.state_str       = megdata_read_str(fd, 16)
        ret.state           = megdata_read_int16(fd)
        # Skip 2 bytes for struct padding
        os.lseek(fd, 2, os.SEEK_CUR)
        # Skip 4 padding bytes in struct
        os.lseek(fd, 4, os.SEEK_CUR)
        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIElectrode\n'
        s += (' ' * indent) + '  Location:       ' + megdata_array_print(self.loc, indent=indent+18) + '\n'
        s += (' ' * indent) + '  Label:          %s\n' % self.lbl
        s += (' ' * indent) + '  State Str:      %s\n' % self.state_str
        s += (' ' * indent) + '  State:          %s (%d)\n' % (BTI_ELEC_STATES.get(self.state, 'INVALID'), self.state)
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

class BTIElectrodeFile(object):
    @classmethod
    def from_file(cls, filename):
        """
        Read a BTI-style electrode file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.electrodes = []

        while True:
            try:
                ret.electrodes.append(BTIElectrode.from_fd(fd))
            except struct.error:
                # End of file
                break

        return ret

    def str_indent(self, indent=0):
        s  = (' ' * indent) + '<BTIElectrodeFile\n'
        for e in self.electrodes:
            s += e.str_indent(indent + 2)
        s += ('>\n')
        return s

    def __str__(self):
        return self.str_indent()

