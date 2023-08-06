import numpy
import os

from .common import *

class CTFPolhemus(object):
    @classmethod
    def from_file(cls, filename):
        """
        Read a CTF Polhemus file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        # We use fd's everywhere else, but here it's easier just to get
        # a file object.  We have to be careful not to close the original
        # fd unexpectedly though as users might get grouchy if we do
        f = os.fdopen(os.dup(fd))

        # For consistency, we also record how many bytes we read and then
        # move the original fd that number of bytes along
        num_bytes = 0

        # Read the number of points
        dat = f.readline()
        num_bytes += len(dat)
        expected_points        = int(dat.strip())
        if expected_points < 1:
            raise ValueError("Fewer than 1 point expected in header of file")

        pts = []
        for p in range(expected_points):
            dat = f.readline()
            num_bytes += len(dat)
            [posnum, x, y, z] = dat.split()
            posnum = int(posnum)
            # Sanity check we're reading the file properly
            if posnum != (p+1):
                raise ValueError("File inconsistency in point number when reading point %d" % (p+1))
            pts.append( [float(x), float(y), float(z)] )

        ret.points = numpy.array(pts, dtype=numpy.float64)

        # Finally, read the fiducials
        ret.fiducial_names     = []
        pts = []
        while True:
            dat = f.readline()
            if len(dat) == 0:
                break
            num_bytes += len(dat)
            [fidname, x, y, z] = dat.split()
            ret.fiducial_names.append(fidname)
            pts.append( [float(x), float(y), float(z)] )

        ret.fiducial_pos = numpy.array(pts, dtype=numpy.float64)
        f.close()
        os.lseek(fd, num_bytes, os.SEEK_CUR)

        return ret

    def str_indent(self, indent=0):
        s = ''
        s += (' ' * indent) + '<CTFPolhemus\n'
        s += (' ' * indent) + '  Num Points:        %d\n' % self.points.shape[0]
        s += (' ' * indent) + '  Points:            ' + megdata_array_print(self.points) + '\n'
        s += (' ' * indent) + '  Num Fiducials      %d\n' % len(self.fiducial_names)
        s += (' ' * indent) + '  Fiducial Names:      \n'
        for f in self.fiducial_names:
            s += (' ' * indent) + '    %s\n' % f
        s += (' ' * indent) + '  Fiducials:         ' + megdata_array_print(self.fiducial_pos) + '\n'
        s += (' ' * indent) + '>\n'
        return s

    def __str__(self):
        return self.str_indent()

