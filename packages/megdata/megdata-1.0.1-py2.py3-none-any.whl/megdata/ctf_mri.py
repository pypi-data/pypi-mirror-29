import os
from numpy import array

from .common import *

class CTFMRIFile(object):
    @classmethod
    def from_file(cls, filename):
        """
        Read a CTF MRI file from a filename
        """
        fd = os.open(filename, os.O_RDONLY)
        ret = cls.from_fd(fd)
        os.close(fd)
        return ret

    @staticmethod
    def cache_from_fd(fd):
        """
        Reads a dictionary of information from the MRI file.

        :param fd: File descriptor.  Must be at start of first tag.
        :type fd: File descriptor.

        :rtype: dict
        :returns: Dictionary of values from file.
        """
        # File format is a tagged list of parameters:
        ## label size (32 bit int)
        ## label (lsize * char)
        ## value type (32 bit int):
        ### 3: position within file (returns last file position) - causes seek
        ### 4: double
        ### 5: int32
        ### 6: int16
        ### 7: uint16
        ### 10: char array: int32 for size, then char array
        # File ends with "EndOfParameters"
        # Read all values into a cache
        cache = {}

        # Wait for EOF to be raised
        while True:
            labelsize = megdata_read_int32(fd)
            label = megdata_read_str(fd, labelsize)

            # File always finishes with EndOfParameters
            if label == 'EndOfParameters':
                break

            valuetype = megdata_read_int32(fd)

            if valuetype == 3:
                vsize = megdata_read_int32(fd)
                value = os.lseek(fd, 0, os.SEEK_CUR)
                # Skip the actual data - we can retrieve it later
                os.lseek(fd, vsize, os.SEEK_CUR)
            elif valuetype == 4:
                value = megdata_read_double(fd)
            elif valuetype == 5:
                value = megdata_read_int32(fd)
            elif valuetype == 6:
                value = megdata_read_int16(fd)
            elif valuetype == 7:
                value = megdata_read_uint16(fd)
            elif valuetype == 10:
                vlength = megdata_read_int32(fd)
                value = megdata_read_str(fd, vlength)
            else:
                raise Exception("Cannot parse CTF MRI value type %d" % valuetype)

            if label in cache:
                cache[label] = [cache[label]]
                cache[label].append(value)
            else:
                cache[label] = value

        return cache

    @staticmethod
    def array_from_string(string, size):
        return array([float(x) for x in string.split('\\')]).reshape(size)

    @staticmethod
    def array_from_cache(cache, key, size):
        if key in cache:
            return CTFMRIFile.array_from_string(cache[key], size)
        else:
            return None

    @classmethod
    def from_fd(cls, fd):
        ret = cls()
        ret.version            = megdata_read_str(fd, 4)
        if ret.version != 'WS1_':
            raise ValueError('Only support WS1_ format MRI files at the moment (%s)' % ret.version)

        # Store the cache on the object for later interrogation
        ret.cache = CTFMRIFile.cache_from_fd(fd)

        cache = ret.cache

        ret.identifier        = cache.get('_CTFMRI_VERSION', None)
        ret.image_size        = cache.get('_CTFMRI_SIZE', None)
        ret.data_size         = cache.get('_CTFMRI_DATASIZE', None)
        ret.orthogonal_flag   = cache.get('_CTFMRI_ORTHOGONALFLAG', None)
        ret.interpolated_flag = cache.get('_CTFMRI_INTERPOLATEDFLAG', None)
        ret.comment           = cache.get('_CTFMRI_COMMENT', None)

        # Don't bother with these for now
        # _SERIES_MODALITY
        # _EQUIP_MANUFACTURER
        # _EQUIP_INSTITUTION
        # _MRIMAGE_IMAGEDNUCLEUS
        # _MRIMAGE_FIELDSTRENGTH
        # _MRIMAGE_ECHOTIME
        # _MRIMAGE_REPETITIONTIME
        # _MRIMAGE_INVERSIONTIME
        # _MRIMAGE_FLIPANGLE

        ret.rotation   = CTFMRIFile.array_from_cache(cache, '_CTFMRI_ROTATE', (3, 1))
        ret.transform  = CTFMRIFile.array_from_cache(cache, '_CTFMRI_TRANSFORMMATRIX', (4, 4))
        ret.mm_per_pix = CTFMRIFile.array_from_cache(cache, '_CTFMRI_MMPERPIXEL', (3, 1))

        ret.hdm_nasion   = CTFMRIFile.array_from_cache(cache, '_HDM_NASION', (3, 1))
        ret.hdm_leftear  = CTFMRIFile.array_from_cache(cache, '_HDM_LEFTEAR', (3, 1))
        ret.hdm_rightear = CTFMRIFile.array_from_cache(cache, '_HDM_RIGHTEAR', (3, 1))
        # x, y, z, radius
        ret.hdm_sphere   = CTFMRIFile.array_from_cache(cache, '_HDM_DEFAULTSPHERE', (4, 1))
        ret.hdm_origin   = CTFMRIFile.array_from_cache(cache, '_HDM_HEADORIGIN', (3, 1))

        # Read in the image data
        ## TODO: We don't need this for now

        return ret
