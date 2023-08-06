#!/usr/bin/python

"""
This file implements the YI FMT-01 MEGHDF file format
"""

from __future__ import unicode_literals

import collections

from copy import deepcopy
from datetime import date, datetime
from time import strptime
from dateutil.parser import parse as parse_iso

# For python2/3 compatibility
from builtins import str as text

import numpy as np
from numpy.linalg import inv

import h5py

try:
    # Python 2
    from builtins import unicode as ustr
except ImportError:
    # Python 3
    from builtins import str as ustr

# For conversions to/from other file formats
from . import BTIPDF, BTIConfigFile, BTI_CHANTYPE_MEG, \
              BTI_CHANTYPE_REFERENCE, BTI_CHANTYPE_EEG, \
              BTI_CHANTYPE_TRIGGER, BTI_CHANTYPE_UTILITY


__all__ = []

def create_subgroup_string_list(parent, dsname, data):
    """
    This is a helper function because creating a dataset consisting
    of a list of strings is slightly annoying
    """

    dt = h5py.special_dtype(vlen=ustr)

    # For some reason in Python3's H5PY, you can't just pass the
    # list in as a named data argument, so loop over it
    ds = parent.create_dataset(dsname, shape=(len(data), ), dtype=dt)

    for x in range(len(data)):
        ds[x] = data[x]

    return ds


####################################################################################
# Acquisition metadata
####################################################################################

class HMEGSubjectData(object):
    """
    This class stores information about the subject.
    """
    def __init__(self):
        self.subject_id = ""
        """
        Textual description of site-specific identifier of subject, dummy value
        set for now
        """

        self.anonymised = True
        """
        Boolean attribute, if true, only metadata will be anonymised
        and subject_id
        For now this value is set as 'True' by default
        """

        self.dob = None
        """
        Date of birth information for subject.  Either None or a datetime.date
        object
        """

        self.name = None
        """
        Subject's name (if available / to be stored)

        Must not contain new-lines
        """

        self.sex = None
        """
        This must be an upper case string describing the subject's sex.

        This may be free-form text, but one of MALE, FEMALE or UNKNOWN MUST
        be used if appropriate
        """

    def anonymise(self):
        """
        Sets anonymised flag and removes all personally identifiable
        information except for subject identifier
        """
        self.anonymised = True
        self.dob = None
        self.name = None
        self.sex = None

    def sanity_check(self):
        if self.dob is not None:
            if not isinstance(self.dob, date):
                raise ValueError("Subject DOB must be a datetime.date object")

        if self.name is not None:
            if '\n' in self.name:
                raise ValueError("Subject name should not contain newline characters")

        return

    def to_hdf5(self, subgroup):
        subgroup.attrs['id'] = ustr(self.subject_id)
        subgroup.attrs['anonymous'] = np.uint8(self.anonymised)

        if self.dob is not None:
            subgroup.attrs['dob'] = self.dob.isoformat()
        if self.name is not None:
            subgroup.attrs['name'] = ustr(self.name)
        if self.sex is not None:
            subgroup.attrs['sex'] = ustr(self.sex)

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):

        ret = cls()

        # Information for which we can have defaults
        ret.subject_id = str(subgroup.attrs.get('id', ''))

        ret.anonymised = bool(subgroup.attrs.get('anonymous', True))

        dob = str(subgroup.attrs.get('dob', ''))
        if dob:
            ret.dob = parse_iso(dob).date()

        ret.name = str(subgroup.attrs.get('name', ''))
        ret.sex = str(subgroup.attrs.get('sex', ''))

        return ret

    def __eq__(self, other):
        if self.anonymised != other.anonymised:
            return False

        if self.subject_id != other.subject_id:
            return False

        if self.dob != other.dob:
            return False

        if self.name != other.name:
            return False

        if self.sex != other.sex:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

__all__.append('HMEGSubjectData')

####################################################################################
# Channel support classes
####################################################################################
class HMEGChannel(object):
    """
    Master class for HDFMEG format channel information
    """
    def __init__(self):
        self.name = ''
        """Channel name (str)"""

        self.chan_type = 'UNKNOWN'
        """Channel Type.  One of ANALOG, COH, DIGITAL, EEG, EEGREF, MEG, MEGREF, UNKNOWN"""

        self.fe_board_type = ''
        """Front-end board type and revision (if known)"""

        self.units = '?'
        """String describing channel units (after scaling)"""

        self.units_per_bit = 1.0
        """Units per bit for channel interpretation"""

        self.aliases = []
        """List of aliases for channel"""

    def __eq__(self, other):
        if self.name != other.name:
            return False

        if self.fe_board_type != other.fe_board_type:
            return False

        if self.chan_type != other.chan_type:
            return False

        if self.units != other.units:
            return False

        if self.units_per_bit != other.units_per_bit:
            return False

        if self.aliases != other.aliases:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def sanity_check(self):
        return

    def __str__(self):
        return '<HMEGChannel %s (%s)>' % (self.name, self.chan_type)

    def to_hdf5(self, subgroup):
        # NB: We assume that the class calling this
        # sets the group name to our name
        subgroup.attrs['chan_type'] = ustr(self.chan_type)
        if self.fe_board_type:
            subgroup.attrs['fe_board_type'] = ustr(self.fe_board_type)
        subgroup.attrs['units'] = ustr(self.units)
        subgroup.attrs['units_per_bit'] = self.units_per_bit
        if len(self.aliases) > 0:
            create_subgroup_string_list(subgroup, 'aliases', self.aliases)

        return subgroup

    def _from_hdf5_internal(self, subgroup):
        """
        Internal routine so that we can reuse the logic in
        subclasses
        """
        self.name = subgroup.name.split('/')[-1]
        self.chan_type = str(subgroup.attrs['chan_type'])
        self.fe_board_type = str(subgroup.attrs.get('fe_board_type', ''))
        self.units = str(subgroup.attrs['units'])
        self.units_per_bit = float(subgroup.attrs['units_per_bit'])
        if 'aliases' in list(subgroup.keys()) and len(subgroup['aliases'].shape) > 0:
            self.aliases = [str(x) for x in subgroup['aliases']]

    @classmethod
    def from_hdf5(cls, subgroup):
        # The specification allows the following channel types:
        # ANALOG, DIGITAL, MEG, MEGREF, EEG, EEGREF, COH

        # We have to work out which of our subclasses to use
        # and return
        if subgroup.attrs['chan_type'] in ['MEG', 'MEGREF']:
            return HMEGMegChannel.from_hdf5(subgroup)
        elif subgroup.attrs['chan_type'] in ['ANALOG', 'DIGITAL']:
            return HMEGADChannel.from_hdf5(subgroup)

        # Otherwise handle just our common fields
        ret = cls()
        ret._from_hdf5_internal(subgroup)

        return ret

    @classmethod
    def from_bti_channel(cls, channel, transform):
        """
        :param channel: A megdata.BTIChannel object
        :param transform: A SCS to CSC affine transformation matrix.  If this
                          is None, the MEG channels will end up remaining in SCS
                          which violates the FMT-01 specification

        :rtype: An HMEGChannel object or one of the more specific derived classes
        """
        from megdata import BTI_CHANTYPE_MEG, BTI_CHANTYPE_REFERENCE, \
                            BTI_CHANTYPE_EEG, BTI_CHANTYPE_TRIGGER, \
                            BTI_CHANTYPE_UTILITY

        # Hand off to HMEGMegChannel for MEG and MEGREF
        # Note that we need to pass the transformation from SCS to CCS down
        if channel.hdr.ctype in [BTI_CHANTYPE_MEG, BTI_CHANTYPE_REFERENCE]:
            return HMEGMegChannel.from_bti_channel(channel, transform)
        elif channel.hdr.ctype in [BTI_CHANTYPE_TRIGGER]:
            return HMEGADChannel.from_bti_channel(channel)

        ret = cls()
        ret.name = channel.hdr.name

        # Channel type
        #  XXX: COH channels?
        if channel.hdr.ctype == BTI_CHANTYPE_EEG:
            ret.chan_type = 'EEG'
        else:
            ret.chan_type = 'UNKNOWN'
        ret.units = channel.hdr.yaxis_label

        return ret

    def get_info_dict(self, ccs_to_scs_transform=None):
        """
        Returns a dictionary containing channel information.

        If ccs_to_scs_transform is provided, any information which is
        stored in CCS will be converted into SCS in the returned
        dictionary

        Fields:
          * name
          * chan_type
          * units_per_bit
          * units
        """
        ret = {}

        ret['name'] = self.name
        ret['chan_type'] = self.chan_type
        ret['units_per_bit'] = self.units_per_bit
        ret['units'] = self.units

        return ret

__all__.append('HMEGChannel')

class HMEGADChannel(HMEGChannel):
    def __init__(self):
        # Common fields
        HMEGChannel.__init__(self)

        # AD-specific fields
        self.mode = ''
        """Must be set to TRIGGER or RESPONSE if appropriate"""

    def __eq__(self, other):
        if HMEGChannel.__eq__(self, other) is not True:
            return False

        if self.mode != other.mode:
            return False

        return True

    def __str__(self):
        return '<HMEGADChannel %s (%s)>' % (self.name, self.chan_type)

    def to_hdf5(self, subgroup):
        # Handle common fields
        subgroup = HMEGChannel.to_hdf5(self, subgroup)

        if self.mode:
            subgroup.attrs['mode'] = ustr(self.mode)

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):
        if subgroup.attrs['chan_type'] not in ['ANALOG', 'DIGITAL']:
            raise ValueError("Incorrect class: HMEGADChannel " \
                             "must have type ANALOG or DIGITAL")

        # Handle the common fields first from
        # our parent class
        ret = cls()
        HMEGChannel._from_hdf5_internal(ret, subgroup)

        # Additional field
        ret.mode = str(subgroup.attrs.get('mode', ''))

        return ret

    @classmethod
    def from_bti_channel(cls, channel):
        from megdata import BTI_CHANTYPE_TRIGGER

        ret = cls()

        ret.name = channel.hdr.name

        if channel.hdr.ctype == BTI_CHANTYPE_TRIGGER:
            ret.chan_type = 'DIGITAL'
            # Annoyingly, we have to look at the channel name for this
            if ret.name == 'TRIGGER':
                ret.mode = 'TRIGGER'
            elif ret.name == 'RESPONSE':
                ret.mode = 'RESPONSE'
            else:
                ret.mode = ''
        else:
            raise ValueError('HMEGADChannel only handles ANALOG and DIGITAL channels')

        return ret

    def get_info_dict(self, ccs_to_scs_transform=None):
        """
        Returns a dictionary containing channel information.

        If ccs_to_scs_transform is provided, any information which is
        stored in CCS will be converted into SCS in the returned
        dictionary

        Additional fields to HMEGChannel.get_info_dict
          * mode
        """
        ret = HMEGChannel.get_info_dict(self)

        ret['mode'] = self.mode

        return ret

__all__.append('HMEGADChannel')


class HMEGMegChannel(HMEGChannel):
    def __init__(self):
        # Common fields
        HMEGChannel.__init__(self)

        # MEG-specific fields
        self.inductance = 0.0
        """Channel Inductance (optional)"""

        self.loop_shape = []
        """Shape of loop for each loop.  CIRCULAR or SQUARE"""

        self.loop_radius = np.zeros((0))
        """Loop radius.  np.ndarray of size (num_loops, )"""

        self.loop_turns = np.zeros((0), dtype=np.float64)
        """Number of turns on loop.  np.ndarray of size (num_loops, )"""

        self.position = np.zeros((0, 3))
        """Position of loops.  np.ndarray of size (num_loops, 3)"""

        self.orientation = np.zeros((0, 3))
        """Orientation of loops.  np.ndarray of size (num_loops, 3)"""

        self.wire_radius = np.zeros((0))
        """Wire radius.  np.ndarray of size (num_loops, )"""

    def __eq__(self, other):
        if HMEGChannel.__eq__(self, other) is not True:
            return False

        if self.inductance != other.inductance:
            return False

        if self.loop_shape != other.loop_shape:
            return False

        if (self.position != other.position).any():
            return False

        if (self.orientation != other.orientation).any():
            return False

        if (self.loop_radius != other.loop_radius).any():
            return False

        if (self.wire_radius != other.wire_radius).any():
            return False

        if (self.loop_turns != other.loop_turns).any():
            return False

        return True

    def sanity_check(self):
        if self.chan_type not in ['MEG', 'MEGREF']:
            raise ValueError('MEG channels must be either MEG or MEGREF type')

        for c in self.loop_shape:
            if c != 'CIRCULAR':
                raise ValueError("Currently only a loop_shape of CIRCULAR is supported")

        if self.num_loops < 1:
            raise ValueError("An MEG channel must have at least one loop")

        if self.position is None or not isinstance(self.position, np.ndarray):
            raise ValueError("Position is not a 2d numpy array")

        if self.position.shape[0] != self.num_loops:
            raise ValueError("Position array and number of loops do not agree (%d vs %d)" % (self.position.shape[0], self.num_loops))

        if self.position.shape[1] != 3:
            raise ValueError("Position array is not three-space")

        if self.orientation is None or not isinstance(self.orientation, np.ndarray):
            raise ValueError("Orientation is not a 2d array")

        if self.orientation.shape[0] != self.num_loops:
            raise ValueError("Orientation array and number of loops do not agree (%d vs %d)" % (self.orientation.shape[0], self.num_loops))

        if self.orientation.shape[1] != 3:
            raise ValueError("Orientation array is not three-space")

        if self.loop_radius is None or not isinstance(self.loop_radius, float):
            raise ValueError("loop_radius is not a float")

        # Optional fields
        if self.wire_radius is not None:
            if self.wire_radius is None or not isinstance(self.wire_radius, float):
                raise ValueError("wire_radius is not a float")

        # Optional fields
        if self.loop_turns is not None:
            if self.loop_turns is None or not isinstance(self.loop_turns, np.ndarray):
                raise ValueError("loop_turns is not a 2d array")

            if self.loop_turns.shape[0] != self.num_loops:
                raise ValueError("Loop turns array and number of loops do not agree (%d vs %d)" % (self.loop_turns.shape[0], self.num_loops))

            if self.loop_turns.shape[1] != 1:
                raise ValueError("Loop turns array does not have a single second dimension")

    def __str__(self):
        return '<HMEGMegChannel %s (%s) (%s turns)>' % (self.name,
                                                        self.chan_type,
                                                        self.num_loops)
    @property
    def num_loops(self):
        return self.position.shape[0]

    def add_loop(self, pos, ori, shape, loop_radius=None, wire_radius=None, loop_turns=None):
        pos = np.array(pos)
        if pos.ndim != 2 or pos.shape != (1, 3):
            raise ValueError('pos must be (1, 3)')

        ori = np.array(ori)
        if ori.ndim != 2 or ori.shape != (1, 3):
            raise ValueError('ori must be (num_loops, 3)')

        if loop_radius is not None:
            loop_radius = np.atleast_1d(np.array(loop_radius))
            if loop_radius.ndim != 1 or len(loop_radius) != 1:
                raise ValueError('loop_radius must be (1, )')

            # If we already have a radius, need to check that it's the same
            if self.loop_radius is not None:
                if self.loop_radius != loop_radius:
                    raise ValueError("loop_radius must be identical for all loops")

        if wire_radius is not None:
            wire_radius = np.atleast_1d(np.array(wire_radius))
            if wire_radius.ndim != 1 or len(wire_radius) != 1:
                raise ValueError('wire_radius must be (1, )')

            # If we already have a radius, need to check that it's the same
            if self.wire_radius is not None:
                if self.wire_radius != wire_radius:
                    raise ValueError("wire_radius must be identical for all loops")

        if loop_turns is not None:
            loop_turns = np.atleast_1d(np.array(loop_turns, dtype=np.float64))
            if loop_turns.ndim != 1 or len(loop_turns) != 1:
                raise ValueError('loop_turns must be single number')

            # If we already have a loop turns, need to check that it's the same
            # XXX: Check that the spec is meant to mandate this
            if self.loop_turns is not None:
                if self.loop_turns != loop_turns:
                    raise ValueError("loop_turns must be identical for all loops")

        # We know we're good by here
        self.position    = np.vstack([self.position, pos])
        self.orientation = np.vstack([self.orientation, ori])
        self.loop_shape.append(str(shape))

        # Update our values with our
        if loop_radius is not None:
            self.loop_radius = np.repeat(loop_radius, (self.position.shape[0]))

        if wire_radius is not None:
            self.wire_radius = np.repeat(wire_radius, (self.position.shape[0]))

        if loop_turns is not None:
            self.loop_turns = np.repeat(loop_turns, (self.position.shape[0]))


    def to_hdf5(self, subgroup):
        # Handle common fields
        subgroup = HMEGChannel.to_hdf5(self, subgroup)

        # All of the below must be datasets
        if self.inductance is not None:
            subgroup.attrs['inductance'] = self.inductance

        create_subgroup_string_list(subgroup, 'loop_shape', self.loop_shape)
        subgroup.create_dataset('loop_radius', data=self.loop_radius)
        subgroup.create_dataset('position',    data=self.position)
        subgroup.create_dataset('orientation', data=self.orientation)
        subgroup.create_dataset('wire_radius', data=self.wire_radius)
        subgroup.create_dataset('loop_turns',  data=self.loop_turns)

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):
        if subgroup.attrs['chan_type'] not in ['MEG', 'MEGREF']:
            raise ValueError("Incorrect class: HMEGMegChannel " \
                             "must have type MEG or MEGREF")

        # Handle the common fields first from
        # our parent class
        ret = cls()
        HMEGChannel._from_hdf5_internal(ret, subgroup)

        # Optional field
        if 'inductance' in list(subgroup.attrs.keys()):
            ret.inductance = float(subgroup.attrs['inductance'])

        # Required fields
        ret.loop_radius  = subgroup['loop_radius'][...]
        ret.loop_shape   = [str(x) for x in subgroup['loop_shape']]
        ret.loop_turns   = subgroup['loop_turns'][...]
        ret.position     = subgroup['position'][...]
        ret.orientation  = subgroup['orientation'][...]
        ret.wire_radius  = subgroup['wire_radius'][...]

        return ret

    @classmethod
    def from_bti_channel(cls, channel, transform):
        """
        :param channel: A megdata.BTIChannel object

        :rtype: A HMEGMegChannel object
        """
        from megdata import BTI_CHANTYPE_MEG, BTI_CHANTYPE_REFERENCE

        ret = cls()

        ret.name = channel.hdr.name

        # Channel type:
        #  Allowable values here: MEG, MEGREF
        if channel.hdr.ctype == BTI_CHANTYPE_MEG:
            ret.chan_type = 'MEG'
        elif channel.hdr.ctype == BTI_CHANTYPE_REFERENCE:
            ret.chan_type = 'MEGREF'
        else:
            raise ValueError('HMEGMegChannel only handles MEG and MEGREF channels')

        # Number of loops
        num_loops = len(channel.chan.loops)

        ret.units_per_bit = channel.hdr.units_per_bit
        ret.units = channel.hdr.yaxis_label

        # Dataset attributes
        # This may go back to single value in REV3 of the spec
        ret.inductance = channel.chan.device.inductance

        for l in range(num_loops):
            # Each position and orientation here is in the subject co-ordinate
            # system.  The FMT01 spec requires the position/orientation to be
            # in the dewar co-ordinate system (which is defined on a
            # per-machine basis)
            position = channel.chan.loops[l].position
            orientation = channel.chan.loops[l].orientation

            # We therefore have to transform the position back to the original
            # co-ordinate frame (dewar)
            if transform is not None:
                newpos = transform.dot(np.hstack([position, [[1.0]]]).T)
                newpos = newpos[0:3].T

                newori = transform.dot(np.hstack([orientation, [[0.0]]]).T)
                newori = newori[0:3].T
                # Ensure that orientation is a unit vector after the transformation
                newori = newori / np.sqrt(np.sum((newori**2)))

                position = newpos
                orientation = newori

            # The BTI units are in ALS; our new units need to be in RAS so each
            # location needs to be transformed

            # Swap to LAS
            position = position[:, (1, 0, 2)]
            orientation = orientation[:, (1, 0, 2)]
            # Flip to RAS
            position[:, 0] *= -1
            orientation[:, 0] *= -1

            # Finally, FMT-01 is in mm, not m; don't convert orientation as this
            # is a unit vector
            position *= 1000.0

            ret.add_loop(position,
                         orientation,
                         'CIRCULAR',
                         channel.chan.loops[l].radius * 1000.0,
                         channel.chan.loops[l].wire_radius * 1000.0,
                         channel.chan.loops[l].turns)

        return ret

    def get_info_dict(self, ccs_to_scs_transform=None):
        """
        Returns a dictionary containing channel information.

        If ccs_to_scs_transform is provided, any information which is
        stored in CCS will be converted into SCS in the returned
        dictionary

        Additional fields to HMEGChannel.get_info_dict
          * inductance
          * loop_shape
          * position
          * orientation
          * loop_radius
          * wire_radius
          * loop_turns
        """
        ret = HMEGChannel.get_info_dict(self)

        ret['inductance'] = self.inductance
        ret['loop_shape'] = self.loop_shape
        ret['loop_radius'] = self.loop_radius
        ret['wire_radius'] = self.wire_radius
        ret['loop_turns'] = self.loop_turns

        if ccs_to_scs_transform is not None:
            # Apply the transform
            ret['position'] = self.get_scs_position(ccs_to_scs_transform)
            ret['orientation'] = self.get_scs_orientation(ccs_to_scs_transform)
        else:
            ret['position'] = self.position
            ret['orientation'] = self.orientation

        return ret

    def get_scs_position(self, transform):
        """
        Returns the position in SCS based on the 4x4 transform matrix provided

        :param transform: np.ndarray (4x4) - affine transformation matrix

        :return: position of channel
        """

        # Transform the position from CCS to SCS
        num_coils = self.position.shape[0]
        pos = np.hstack([self.position, np.ones((num_coils, 1))])
        pos = transform.dot(pos.T).T

        return pos[:, 0:3]

    def get_scs_orientation(self, transform):
        """
        Returns the orientation in SCS based on the 4x4 transform matrix provided

        :param transform: np.ndarray (4x4) - affine transformation matrix

        :return: orientation of channel
        """

        # Transform the position from CCS to SCS
        num_coils = self.orientation.shape[0]
        ori = np.hstack([self.orientation, np.zeros((num_coils, 1))])
        ori = transform.dot(ori.T).T
        ori = ori[:, 0:3]

        # Check that this is a unit vector
        ori = ori / np.atleast_2d(np.sqrt(np.sum((ori**2), axis=1))).T

        return ori

__all__.append('HMEGMegChannel')

############################################################################
# System configuration objects
############################################################################

class HMEGProtocol(object):
    def __init__(self):
        self.protocol_name = ''
        """Protocol name"""

        self.initiating_user = ''
        """User who started the acquisition"""

        self.definition = ''
        """YAML definition of protocol (in YI FMT-30)"""

    def __eq__(self, other):
        if self.protocol_name != other.protocol_name:
            return False

        if self.initiating_user != other.initiating_user:
            return False

        if self.definition != other.definition:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def sanity_check(self):
        return

    def to_hdf5(self, subgroup):
        if self.protocol_name:
            subgroup.attrs['protocol_name'] = ustr(self.protocol_name)
        if self.initiating_user:
            subgroup.attrs['initiating_user'] = ustr(self.initiating_user)
        if self.definition:
            subgroup.attrs['definition'] = ustr(self.definition)

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        ret.protocol_name   = str(subgroup.attrs.get('protocol_name', ''))
        ret.initiating_user = str(subgroup.attrs.get('initiating_user', ''))
        ret.definition      = str(subgroup.attrs.get('definition', ''))

        return ret


class HMEGWeightTable(object):
    def __init__(self):
        self.description = ''
        """Description of weight table"""

        self.created = None
        """datetime.datetime object of creation date of table"""

        self.ref_chans = []
        """List of text names of the source channels for the table"""

        self.tgt_chans = []
        """List of text names of the target channels for the table"""

        self.weights = None
        """np.array of weighting factors (ref_chans, tgt_chans)"""

    def __eq__(self, other):
        if self.description != other.description:
            return False

        if self.created != other.created:
            return False

        if self.ref_chans != other.ref_chans:
            return False

        if self.tgt_chans != other.tgt_chans:
            return False

        if (self.weights != other.weights).any():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def sanity_check(self):
        if (len(self.ref_chans) == 0) and (len(self.tgt_chans == 0)):
            if self.weights is None:
                return
            else:
                raise ValueError("Weights matrix set without src and tgt channels being set")

        if self.weights is None:
            raise ValueError("Some src or tgt channels set but no weights matrix set")

        if (not isinstance(self.weights, np.ndarray) or (self.weights.ndim != 2)):
            raise ValueError("Weights matrix is not a 2d array")

        if len(self.ref_chans) != self.weights.shape[0]:
            raise ValueError("Weight matrix shape[0] != number of source channels")

        if len(self.tgt_chans) != self.weights.shape[1]:
            raise ValueError("Weight matrix shape[1] != number of target channels")

    def to_hdf5(self, subgroup):
        if self.description:
            subgroup.attrs['description'] = ustr(self.description)
        if self.created:
            subgroup.attrs['created'] = self.created.isoformat()

        # Datasets
        create_subgroup_string_list(subgroup, 'ref_chans', self.ref_chans)
        create_subgroup_string_list(subgroup, 'tgt_chans', self.tgt_chans)
        subgroup.create_dataset('weights', data=self.weights)

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        ret.description = str(subgroup.attrs.get('description', ''))

        if 'created' in list(subgroup.attrs.keys()):
            # Use the dateutil parser to parse ISO8601
            ret.created = parse_iso(subgroup.attrs['created'])

        ret.ref_chans = [str(x) for x in subgroup['ref_chans']]
        ret.tgt_chans = [str(x) for x in subgroup['tgt_chans']]
        ret.weights = subgroup['weights'][...]

        return ret

__all__.append('HMEGWeightTable')


class HMEGSystemConfig(object):
    """
    This class stores configuration information about the scanner used.

    The most important information stored in this class are the channel
    specification parameters and the system to subject transformation
    information.
    """
    def __init__(self):
        # TODO: Argue with Nat that this needs to be optional
        self.software_version = ''
        """
        Software version used to record dataset
        """

        # TODO: Argue with Nat that this needs to be optional
        self.model = ''
        """
        Textual description of the system model
        """

        self.location = ''
        """
        Textual description of the system location
        """

        self.name = ''
        """
        Textual description of the system name
        """

        # TODO: This is currently mandatory in the spec
        self.supply_freq = None
        """
        Mains frequency of the system (if known)
        """

        # TODO: Argue with Nat that this needs to be optional
        self.site_id = 'N/K'
        """
        Originating site/installation identifier
        """

        self.channels = {}
        """
        Dictionary mapping channel names to channel descriptions.

        Each entry must be a class derived from HMEGChannel: at present
        the supported classes are:
          * HMEGChannel for EEG, COH and UNKNOWN channel types
          * HMEGADChannel for ANALOG and DIGITAL channel types
          * HMEGMegChannel for MEG and MEGREF channel types
        """

        self.protocol = HMEGProtocol()

        self.weights_tables = {}
        """
        Dictionary of weights tables.  Each entry must be a HMEGWeightTable
        object.

        Table naming and meaning is system-dependent.
        """

    def __eq__(self, other):
        if self.software_version != other.software_version:
            return False

        if self.model != other.model:
            return False

        if self.location != other.location:
            return False

        if self.name != other.name:
            return False

        if self.supply_freq != other.supply_freq:
            return False

        if sorted(self.channels.keys()) != sorted(other.channels.keys()):
            return False

        for c in list(self.channels.keys()):
            if self.channels[c] != other.channels[c]:
                return False

        if sorted(self.weights_tables.keys()) != sorted(other.weights_tables.keys()):
            return False

        if self.protocol != other.protocol:
            return False

        for w in list(self.weights_tables.keys()):
            if self.weights_tables[w] != other.weights_tables[w]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def sanity_check(self):
        if self.supply_freq is not None:
            if not isinstance(self.supply_freq, float):
                raise ValueError("Mains frequency is not a float")

        return

    def to_hdf5(self, subgroup):
        subgroup.attrs['software_version'] = ustr(self.software_version)
        subgroup.attrs['model'] = ustr(self.model)
        subgroup.attrs['location'] = ustr(self.location)
        subgroup.attrs['name'] = ustr(self.name)
        subgroup.attrs['site_id'] = ustr(self.site_id)

        # TODO: Currently this is mandatory in the spec
        if self.supply_freq is not None:
            subgroup.attrs['supply_freq'] = self.supply_freq

        # Write channels in a sorted order
        channel_info = subgroup.create_group('channels')
        for channame in sorted(self.channels.keys()):
            channel = self.channels[channame]
            channel.to_hdf5(channel_info.create_group(ustr(channame)))

        self.protocol.to_hdf5(subgroup.create_group('protocol'))

        # Also sort weights output
        weights = subgroup.create_group('weights')
        for wtable_name in sorted(self.weights_tables.keys()):
            wtable = self.weights_tables[wtable_name]
            wtable.to_hdf5(weights.create_group(wtable_name))

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        # Information for which we can have defaults
        ret.name = str(subgroup.attrs.get('name', ''))
        ret.model = str(subgroup.attrs.get('model', ''))
        ret.location = str(subgroup.attrs.get('location', ''))
        ret.software_version = str(subgroup.attrs.get('software_version', ''))

        # Leave this as None if not present
        if 'supply_freq' in list(subgroup.attrs.keys()):
            ret.supply_freq = float(subgroup.attrs.get('supply_freq'))

        for channame, cgrp in subgroup['channels'].items():
            ret.channels[channame] = HMEGChannel.from_hdf5(cgrp)

        if 'protocol' in subgroup:
            ret.protocol = HMEGProtocol.from_hdf5(subgroup['protocol'])

        # Grab the weights tables back in
        for wtable_name, wgrp in subgroup['weights'].items():
            ret.weights_tables[wtable_name] = HMEGWeightTable.from_hdf5(wgrp)

        return ret

    @classmethod
    def from_bti_config(cls, bti_config, skip_transform=False):
        """
        :param bti_config: A megdata.BTIConfigFile object
        :param skip_transform: Skips the SCS to CCS transform stage for MEG
                               channels

        :rtype: A filled-in HMEGSystemConfig object
        """

        ret = cls()

        # Fill in the metadata
        ret.name = bti_config.hdr.dap_hostname
        ret.location = bti_config.hdr.sitename
        ret.model = bti_config.hdr.get_systype_string()
        ret.software_version = bti_config.hdr.version    #probably what we want
        ret.supply_freq = float(bti_config.hdr.supply_freq)

        # We need to work our our SCS to CCS transformation for the
        # 4D system.  This is done by finding the transform in the
        # bti config object
        if skip_transform:
            transform = None
        else:
            if len(bti_config.transforms) != 1:
                raise Exception("Did not find exactly one transform in config object")

            transform = bti_config.transforms[0].copy()

            # Before inverting, need to ensure that last row is [0, 0, 0, 1]
            # as the 4D software does not write it out correctly
            transform[3, :] = [0, 0, 0, 1.0]

            transform = inv(transform)

        # Fill in all off the channels first
        for channel in bti_config.channels:
            channame = channel.hdr.name
            hchan = HMEGChannel.from_bti_channel(channel, transform)
            ret.channels[channame] = hchan

        # Find any weighting tables
        for block in bti_config.user_blocks:
            # E-tables
            if block.hdr.blocktype == 'B_E_table_used':
                et = HMEGWeightTable()
                et.name = 'Etable'
                et.ref_chans = block.data.e_chan_names
                et.tgt_chans = block.data.chan_names
                # We are required to store these as float64 by the MEGHDF5 spec
                et.weights = block.data.etable.astype(np.float64)
                ret.weights_tables['Etable'] = et
            # Analog and DSP weights
            elif block.hdr.blocktype == 'B_weights_used':
                aw = HMEGWeightTable()
                aw.name = 'analog'
                aw.ref_chans = block.data.analog_chan_names
                aw.tgt_chans = block.data.chan_names
                # We are required to store these as float64 by the MEGHDF5 spec
                aw.weights = block.data.analog_wts.astype(np.float64)
                ret.weights_tables['analog'] = aw

                dw = HMEGWeightTable()
                dw.name = 'digital'
                dw.ref_chans = block.data.dsp_chan_names
                dw.tgt_chans = block.data.chan_names
                dw.weights = block.data.dsp_wts.astype(np.float64)
                ret.weights_tables['digital'] = dw

        return ret

    def __str__(self):
        s = '<HMEGSystemConfig '
        if len(self.name) > 0:
            s += self.name + ' '
        if len(self.location) > 0:
            s += '(%s) ' % self.location
        if len(self.model) > 0:
            s += '[%s] ' % self.model
        if len(self.software_version) > 0:
            s += '[%s] ' % self.software_version
        if self.supply_freq is not None:
            s += '\n  Mains Freq: %.2f' % self.supply_freq

        s += '\n  Channels: '
        s += ','.join(sorted(list(self.channels.keys())))

        if len(self.weights_tables) > 0:
            s += '\n  Weights tables: ' + ','.join(self.weights_tables.keys())

        s += '\n>'

        return s

__all__.append('HMEGSystemConfig')

############################################################################
# Geometry objects
############################################################################

class HMEGGeomFiducials(object):
    def __init__(self):
        self.fiducials = []
        """List of fiducial names.

        Common abbreviations are:
            * LPA: Left pre-auricular point
            * RPA: Right pre-auricular point
            * Nasion: Nasion
            * Cz: Vertex (often used incorrectly in MEG)
            * In: Inion (often used incorrectly in MEG)
        """

        self.points = np.zeros((0, 3))
        """np.array of fiducial points (num_pts, 3)"""

    def __eq__(self, other):
        if self.fiducials != other.fiducials:
            return False

        if (self.points != other.points).any():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def sanity_check(self):
        if (not isinstance(self.points, np.ndarray) or (self.points.ndim != 2)):
            raise ValueError("Points matrix is not a 2d array")

        if self.points.shape[1] != 3:
            raise ValueError("Points matrix shape[1] != 3")

        if len(self.fiducials) != self.points.shape[0]:
            raise ValueError("Points matrix shape[0] != number of points")

        for pos in self.fiducials:
            if pos.find(',') != -1:
                raise ValueError("Position name '%s' contains a ," % pos)

    def to_hdf5(self, subgroup):
        for fididx in range(len(self.fiducials)):
            # Each fiducial is now stored in a group
            name = self.fiducials[fididx]
            # The loc must be (1, 3)
            loc  = self.points[fididx:fididx+1, :]
            grp = subgroup.create_group(name)
            grp.create_dataset('location', data=loc)

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        for fiducial in list(subgroup.keys()):
            loc = subgroup[fiducial]['location'][...]
            ret.fiducials.append(fiducial)
            ret.points = np.vstack([ret.points, loc])

        return ret

    @classmethod
    def from_bti_config(cls, bti_config):
        """
        :param bti_config: A megdata.BTIConfigFile object

        :rtype: A filled-in HMEGGeomFiducials object or
                None if can't find relevant information
        """

        BTI_NAME_TRANSFORM = {'L': 'LPA', 'R': 'RPA', 'N': 'Nasion',
                              'C': 'Cz', 'I': 'In'}

        for block in bti_config.user_blocks:
            if block.hdr.blocktype == 'b_eeg_elec_locs':
                ret = cls()
                names = []
                pos = []
                for elec in block.data.electrodes:
                    # Only store the basic fiducial information here
                    if elec.label not in BTI_NAME_TRANSFORM:
                        continue
                    # Transform the name if we know it
                    names.append( BTI_NAME_TRANSFORM.get(elec.label, elec.label) )

                    # The position needs to be changed from ALS to RAS
                    loc = elec.location
                    # Convert to LAS
                    loc = loc[:, [1, 0, 2]]
                    # Flip left/right
                    loc[:, 0] *= -1.0
                    # Convert to mm instead of m
                    loc *= 1000.0

                    pos.append(np.squeeze(loc))

                ret.fiducials = names
                # This should give us a (pos, 3) array
                ret.points = np.array(pos)

                return ret

        return None

    def __str__(self):
        s = '<HMEGGeomFiducials '
        for p in range(len(self.fiducials)):
            s += '\n  %s: (%.3e, %.3e, %.3e)' % (self.fiducials[p],
                                                 self.points[p, 0],
                                                 self.points[p, 1],
                                                 self.points[p, 2])
        s += '>'

        return s

__all__.append('HMEGGeomFiducials')


class HMEGGeomCoils(object):
    def __init__(self):
        self.coil_names = []
        """List of coil names.

        Most commonly this will be Coil1, Coil2, ...
        """

        self.points = np.zeros((0, 3))
        """np.array of coil points (num_coils, 3)"""

    def __eq__(self, other):
        if self.coil_names != other.coil_names:
            return False

        if (self.points != other.points).any():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def sanity_check(self):
        if (not isinstance(self.points, np.ndarray) or (self.points.ndim != 2)):
            raise ValueError("Points matrix is not a 2d array")

        if self.points.shape[1] != 3:
            raise ValueError("Points matrix shape[1] != 3")

        if len(self.coil_names) != self.points.shape[0]:
            raise ValueError("Points matrix shape[0] != number of points")

        for coil in self.coil_names:
            if coil.find(',') != -1:
                raise ValueError("Coil name '%s' contains a ," % coil)

    def to_hdf5(self, subgroup):
        for coilidx in range(len(self.coil_names)):
            # Each coil is now stored in a group
            name = self.coil_names[coilidx]
            # The loc must be (1, 3)
            loc  = self.points[coilidx:coilidx+1, :]
            grp = subgroup.create_group(name)
            grp.create_dataset('location', data=loc)

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        for coilname in list(subgroup.keys()):
            loc = subgroup[coilname]['location'][...]
            ret.coil_names.append(coilname)
            ret.points = np.vstack([ret.points, loc])

        return ret

    @classmethod
    def from_bti_config(cls, bti_config):
        """
        :param bti_config: A megdata.BTIConfigFile object

        :rtype: A filled-in HMEGGeomCoils object or
                None if can't find relevant information
        """

        for block in bti_config.user_blocks:
            if block.hdr.blocktype == 'b_eeg_elec_locs':
                ret = cls()
                names = []
                pos = []
                for elec in block.data.electrodes:
                    # Skip non-coil locations - we store them in a different class
                    if not elec.label.startswith('Coil'):
                        continue

                    names.append(elec.label)

                    # The position needs to be changed from ALS to RAS
                    loc = elec.location
                    # Convert to LAS
                    loc = loc[:, [1, 0, 2]]
                    # Flip left/right
                    loc[:, 0] *= -1.0
                    # Convert to mm instead of m
                    loc *= 1000.0

                    pos.append(np.squeeze(loc))

                ret.coil_names = names
                # This should give us a (pos, 3) array
                ret.points = np.array(pos)

                return ret

        return None

    def __str__(self):
        s = '<HMEGGeomCoils '
        for p in range(len(self.coil_names)):
            s += '\n  %s: (%.3e, %.3e, %.3e)' % (self.coil_names[p],
                                                 self.points[p, 0],
                                                 self.points[p, 1],
                                                 self.points[p, 2])
        s += '>'

        return s

__all__.append('HMEGGeomCoils')

class HMEGGeomEEG(HMEGGeomCoils):
    # This is the same as Coils but with EEG coil information
    def __str__(self):
        s = '<HMEGGeomEEG '
        for p in range(len(self.coil_names)):
            s += '\n  %s: (%.3e, %.3e, %.3e)' % (self.coil_names[p],
                                                 self.points[p, 0],
                                                 self.points[p, 1],
                                                 self.points[p, 2])
        s += '>'

        return s

    @classmethod
    def from_bti_config(cls, bti_config):
        """
        :param bti_config: A megdata.BTIConfigFile object

        :rtype: A filled-in HMEGGeomEEG object or
                None if can't find relevant information
        """
        # These are fiducials and shouldn't be stored here
        KNOWN_NAMES = ['L', 'R', 'N', 'C', 'I']

        for block in bti_config.user_blocks:
            if block.hdr.blocktype == 'b_eeg_elec_locs':
                ret = cls()
                names = []
                pos = []
                for elec in block.data.electrodes:
                    # Only take non-coil, non-fiducial points
                    if elec.label in KNOWN_NAMES or \
                       elec.label.startswith('Coil'):
                           continue

                    names.append(elec.label)

                    # The position needs to be changed from ALS to RAS
                    loc = elec.location
                    # Convert to LAS
                    loc = loc[:, [1, 0, 2]]
                    # Flip left/right
                    loc[:, 0] *= -1.0
                    # Convert to mm instead of m
                    loc *= 1000.0

                    pos.append(np.squeeze(loc))

                ret.coil_names = names
                # This should give us a (pos, 3) array
                ret.points = np.array(pos)

                return ret


class HMEGGeomHeadshape(object):
    def __init__(self):
        self.points = np.zeros((0, 3))
        """np.array of coil points (num_pts, 3)"""

    def __eq__(self, other):
        if (self.points != other.points).any():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def sanity_check(self):
        if (not isinstance(self.points, np.ndarray) or (self.points.ndim != 2)):
            raise ValueError("Points matrix is not a 2d array")

        if self.points.shape[1] != 3:
            raise ValueError("Points matrix shape[1] != 3")

    def to_hdf5(self, subgroup):
        if self.points.shape[0] > 0:
            subgroup.create_dataset('head_shape', data=self.points)

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        if 'head_shape' in list(subgroup.keys()):
            ret.points = subgroup['head_shape'][...]

        return ret

    @classmethod
    def from_bti_hsfile(cls, bti_hsfile):
        """
        :param bti_hsfile: A megdata.BTIHSFile object

        :rtype: A filled-in HMEGGeomHeadshape object
        """

        ret = cls()

        # Need to re-order the digitisation points
        # 4D has them as ALS, we want them as RAS
        ret.points = bti_hsfile.dig_points
        # Convert to LAS
        ret.points = ret.points[:, [1, 0, 2]]
        # Flip left/right
        ret.points[:, 0] *= -1.0
        # Convert to mm instead of m
        ret.points *= 1000.0

        return ret

    def __str__(self):
        s = '<HMEGGeomHeadshape \n'
        if self.points.shape[0] > 0:
            s += str(self.points)
        s += '\n>'

        return s

__all__.append('HMEGGeomHeadshape')


############################################################################
# Data acquisition objects
############################################################################

# Valid acquisition types
ACQ_TYPES = ['EMPTY', 'ACQ', 'COH', 'EEG_IMPEDANCE', 'UNKNOWN']

class HMEGAcquisitions(object):
    """
    Class containing metadata about all of the acquisitions.
    """
    def __init__(self):
        self.start_time = None
        """Start time of the protocol (datetime object)"""

        self.acquisitions = {}
        """Dictionary of acquisition objects"""

        self.default_acq_name = None
        """Default acquisition name (key into dictionary)"""

    def __eq__(self, other):
        if self.default_acq_name != other.default_acq_name:
            return False

        if len(self.acquisitions) != len(other.acquisitions):
            return False

        if sorted(self.acquisitions.keys()) != sorted(other.acquisitions.keys()):
            return False

        for aname in list(self.acquisitions.keys()):
            ok = self.acquisitions[aname] == other.acquisitions[aname]
            if not ok:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def default_acq(self):
        return self.acquisitions[self.default_acq_name]

    def sanity_check(self):
        if self.default_acq_name is not None:
            if self.default_acq_name not in list(self.acquisitions.keys()):
                raise ValueError("Default acquisition name %s unknown" % self.default_acq_name)

    def to_hdf5(self, subgroup, compress=False):
        if self.start_time is not None:
            subgroup.attrs['start_time'] = ustr(self.start_time.isoformat())

        for run_name in list(self.acquisitions.keys()):
            self.acquisitions[run_name].to_hdf5(subgroup.create_group(run_name), compress)

        if self.default_acq_name is not None and \
                self.default_acq_name in list(self.acquisitions.keys()):
            subgroup['default'] = h5py.SoftLink('/acquisitions/%s' % self.default_acq_name)

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        # Use the dateutil parser to parse ISO8601
        if 'start_time' in list(subgroup.attrs.keys()):
            ret.start_time = parse_iso(subgroup.attrs['start_time'])

        for run_name in list(subgroup.keys()):
            if run_name == 'default':
                # Have to use the low level interface here by reading it
                # out and stripping off the name
                linktgt = subgroup.id.get_linkval('default').split('/')[-1]

                ret.default_acq_name = linktgt
            else:
                ret.acquisitions[str(run_name)] = HMEGAcquisition.from_hdf5(subgroup[str(run_name)])

        return ret

__all__.append('HMEGAcquisitions')


class HMEGAcquisition(object):
    """
    Class containing data for a single acquisition.
    """
    def __init__(self):
        # Attributes
        self.acq_type = 'UNKNOWN'
        """
        Textual description of acquisition type

        Valid values are:
        EMPTY, COH, ACQ, EEG_IMPEDANCE, UNKNOWN
        """

        self.sequence = 1
        """
        Protocol acquisition step number.  Note that these
        may not be consecutive.
        """

        self.description = ''
        """
        String describing acquisition.
        """

        self.start_time = None
        """
        Start time of acquisition
        """

        self.sample_rate = None
        """
        Sample rate of data in Hz
        """

        self.upb_applied = False
        """
        Have the UPB been applied?
        """

        self.weights_configured = ''
        """
        Weights used during acquisition
        """

        self.weights_applied = ''
        """
        Have weights already been applied to data
        """

        self.coh_active = False
        """
        Were COH in use during this acquisition
        """

        self.subject_position = 'SEATED'
        """
        Position of subject during acquisition
        """

        # Datasets
        self.channel_list = []
        """
        List of channel names in order contained within dataset.

        Defines num_channels
        """

        self.bad_channel_list = []
        """
        List of known bad channel names contained within dataset.
        """

        self.ccs_to_scs_transform = np.eye(4)
        """
        Cryostat co-ordinate system to subject co-ordinate system transform.
        For use with MEG and MEGREF channel positions
        """

        self.data = np.zeros((0, 0))
        """
        Dataset containing data.  Must be of size (num_pts, num_channels).

        May be of the following types: int16, int32, float32, float64
        """

        self.epochs = None
        """
        Can be an HMEGAcquisitionEpochs object
        """

    def __deepcopy__(self, memo):
        from copy import deepcopy
        # We can just copy most things (except data)
        new = self.__class__()

        new.acq_type = deepcopy(self.acq_type, memo)
        new.sequence = deepcopy(self.sequence, memo)
        new.description = deepcopy(self.description, memo)
        new.start_time = deepcopy(self.start_time, memo)
        new.sample_rate = deepcopy(self.sample_rate, memo)
        new.upb_applied = deepcopy(self.upb_applied, memo)
        new.weights_configured = deepcopy(self.weights_configured, memo)
        new.weights_applied = deepcopy(self.weights_applied, memo)
        new.coh_active = deepcopy(self.coh_active, memo)
        new.subject_position = deepcopy(self.subject_position, memo)
        new.channel_list = deepcopy(self.channel_list, memo)
        new.bad_channel_list = deepcopy(self.bad_channel_list, memo)
        new.ccs_to_scs_transform = deepcopy(self.ccs_to_scs_transform, memo)
        new.epochs = deepcopy(self.epochs, memo)

        if isinstance(self.data, h5py.Dataset):
            # Copy the reference as we're looking at an existing dataset
            # and don't hold the data in memory
            new.data = self.data
        else:
            # Deep copy the data as requested
            new.data = deepcopy(self.data, memo)

        return new

    def __eq__(self, other):
        if self.acq_type != other.acq_type:
            return False

        if self.sequence != other.sequence:
            return False

        if self.description != other.description:
            return False

        if self.sample_rate != other.sample_rate:
            return False

        if self.start_time != other.start_time:
            return False

        if self.upb_applied != other.upb_applied:
            return False

        if self.weights_configured != self.weights_configured:
            return False

        if self.weights_applied != self.weights_applied:
            return False

        if self.coh_active != self.coh_active:
            return False

        if self.subject_position != self.subject_position:
            return False

        # Datasets
        if self.channel_list != other.channel_list:
            return False

        if self.bad_channel_list != other.bad_channel_list:
            return False

        if (self.data[...] != other.data[...]).any():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def sample_period(self):
        return 1.0/self.sample_rate

    @property
    def num_channels(self):
        return len(self.channel_list)

    @property
    def num_samples(self):
        return self.data.shape[0]

    def sanity_check(self):
        if self.acq_type not in ['EMPTY', 'COH', 'ACQ', 'EEG_IMPEDANCE', 'UNKNOWN']:
            raise ValueError("Acquisition type %s not known" % self.acq_type)

        if len(self.data.shape) != 2:
            raise ValueError("Data array must be 2D")

        if len(self.channel_list) != self.data.shape[1]:
            raise ValueError("Channel list and data array do not have same num_chans")

        for channel in self.bad_channel_list:
            if channel not in self.channel_list:
                raise ValueError("bad_channel %s not in channel list" % channel)

    def to_hdf5(self, subgroup, compress=False):
        subgroup.attrs['acq_type'] = ustr(self.acq_type)

        subgroup.attrs['sequence'] = np.uint32(self.sequence)

        if self.description:
            subgroup.attrs['description'] = ustr(self.description)

        subgroup.attrs['sample_rate'] = self.sample_rate

        if self.start_time is not None:
            subgroup.attrs['start_time'] = ustr(self.start_time.isoformat())

        subgroup.attrs['upb_applied'] = np.uint8(self.upb_applied)

        subgroup.attrs['weights_configured'] = ustr(self.weights_configured)
        subgroup.attrs['weights_applied'] = ustr(self.weights_applied)
        subgroup.attrs['coh_active'] = np.uint8(self.coh_active)
        subgroup.attrs['subject_position'] = ustr(self.subject_position)

        # Groups
        create_subgroup_string_list(subgroup, 'channel_list', self.channel_list)

        if len(self.bad_channel_list) > 0:
            create_subgroup_string_list(subgroup, 'bad_channel_list', self.bad_channel_list)

        # Don't try and create empty datasets
        # We deal with this properly on the reading side too
        if self.data.shape[0] > 0:
            if compress:
                subgroup.create_dataset('data', data=self.data, compression='gzip', shuffle=True)
            else:
                subgroup.create_dataset('data', data=self.data)

        subgroup.create_dataset('ccs_to_scs_transform', data=self.ccs_to_scs_transform)

        if self.epochs is not None:
            self.epochs.to_hdf5(subgroup.create_group('epochs'))

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        # Deal with default entries for this
        ret.acq_type = str(subgroup.attrs.get('acq_type', 'UNKNOWN'))

        # Can't use default as don't want to cast None to int
        if 'sequence' in list(subgroup.attrs.keys()):
            ret.sequence = int(subgroup.attrs.get('sequence'))

        ret.description = str(subgroup.attrs.get('description', ''))

        # There's no sane default for this
        ret.sample_rate = float(subgroup.attrs.get('sample_rate'))

        # Use dateutil to parse ISO time
        if 'start_time' in list(subgroup.attrs.keys()):
            ret.start_time = parse_iso(subgroup.attrs['start_time'])

        ret.upb_applied = bool(subgroup.attrs.get('upb_applied', 0))

        ret.weights_configured = str(subgroup.attrs.get('weights_configured', ''))
        ret.weights_applied = str(subgroup.attrs.get('weights_applied', ''))
        ret.coh_active = bool(subgroup.attrs.get('coh_active', False))
        ret.subject_position = str(subgroup.attrs.get('subject_position', ''))

        ret.channel_list = [str(x) for x in subgroup['channel_list']]
        if 'bad_channel_list' in list(subgroup.keys()):
            ret.bad_channel_list = [str(x) for x in subgroup['bad_channel_list']]

        # We take references to the arrays rather than reading
        # in all of the data
        # Note that this means the file needs to be held open as long as
        # we might access the data.
        if 'data' in list(subgroup.keys()):
            ret.data = subgroup['data']

        if 'ccs_to_scs_transform' in subgroup:
            ret.ccs_to_scs_transform = subgroup['ccs_to_scs_transform'][...]
        else:
            ret.ccs_to_scs_transform = np.eye(4)

        if 'epochs' in list(subgroup.keys()):
            ret.epochs = HMEGAcquisitionEpochs.from_hdf5(subgroup['epochs'])

        return ret

    @classmethod
    def from_bti_pdf(cls, bti_pdf, bti_config, acq_index, acq_type, applyupb=False):
        """
        :param bti_pdf: A megdata.BTIPDF object
        :param bti_config: The relevant megdata.BTIConfigFile object
        :param acq_type: One of the valid acquisition types
        :param applyupb: Apply UPB and convert data to float64

        :rtype: A filled-in HMEGAcquisition object
        """

        ret = cls()

        ret.acq_type = acq_type

        ret.sequence = acq_index

        # Take the last filename as a default description
        ret.description = bti_pdf.processes[-1].filename

        ret.sample_rate = 1.0 / bti_pdf.hdr.sample_period

        # Use B_file_create process to determine start time
        ret.start_time = None
        for proc in bti_pdf.processes:
            if proc.hdr.processtype == 'B_file_create':
                # Use this as the start time
                ret.start_time = datetime.fromtimestamp(proc.timestamp)

        ret.upb_applied = 0

        # The user is responsible for filling in these fields
        ret.weights_configured = ''
        ret.weights_applied = ''

        if ret.acq_type == 'COH':
            ret.coh_active = True
        else:
            ret.coh_active = False

        # XXX: Figure out if we can find out the subject position
        ret.subject_position = ''
        for proc in bti_config.user_blocks:
            if proc.hdr.blocktype == 'B_weights_used':
                # Only store this if we have a known position
                pos = proc.data.hdr.name.upper()
                if pos in ['SEATED', 'SUPINE']:
                    ret.subject_position = pos

        # This must be in the order in which the data is stored

        # Note that we need to take the channel list names from
        # the config, not the PDF, otherwise channels can end up
        # incorrectly named (especially in COH runs)
        # Note that the chan_no field is 1-indexed (go figure)
        # so we need to offset our lookup into the config channels
        # structure
        ret.channel_list = [ bti_config.channels[c.chan_no - 1].hdr.name \
                                for c in bti_pdf.channels ]

        # As a sanity check, we ensure that we don't have the same channel
        # name more than once - this is invalid
        if len(set(ret.channel_list)) != len(ret.channel_list):
            duplicates = ','.join(sorted([name for name, count \
                               in list(collections.Counter(ret.channel_list).items()) \
                               if count > 1]))
            raise ValueError("Channel list contains duplicate values for %s" % duplicates)

        # TODO: bad_channel_list (if we have information for it)
        ret.data = bti_pdf.read_raw_data()

        if np.issubdtype(np.floating, ret.data.dtype):
            # In the case that we already have floating point data, the
            # UPB have already been applied, so just note this

            # NB: rev6 of FMT-01 only allows float64, so convert data to
            # 64-bit.  A future revision will allow float32 as well
            ret.data = ret.data.astype(np.float64)

            # Note that UPB are applied
            ret.upb_applied = 1

        elif applyupb:
            # We must have integer data, so we need to apply the UPB

            # First of all, convert data to float64
            ret.data = ret.data.astype(np.float64)

            # Now apply the UPB
            upb = [ bti_config.channels[c.chan_no - 1].hdr.units_per_bit \
                                for c in bti_pdf.channels ]

            ret.data = ret.data * upb

            # And note that UPB are applied
            ret.upb_applied = 1

        # As a further sanity check, check that our number of channels and data
        # sizes are sensible
        if ret.data.shape[1] != len(ret.channel_list):
            raise ValueError("Channel list (%d) and data (%d) disagree on number of channels" % \
                              (ret.data.shape[1], len(ret.channel_list)))

        ret.epochs = HMEGAcquisitionEpochs.from_bti_pdf(bti_pdf)

        return ret

__all__.append('HMEGAcquisition')


class HMEGAcquisitionEpochs(object):
    def __init__(self):
        self.channel_ids = []
        """
        List of channel IDs used to generate each of the trigger values
        """

        self.trigger_codes = []
        """
        List of epoch codes.
        Must be length num_epochs
        If empty or missing, no epoching information is avilable.
        """

        self.trigger_labels = []
        """
        List of trigger labels (strings describing the trigger)
        """

        self.sample_indexes = np.zeros((0, 3), np.uint64)
        """
        Dataset containing epoching information if available.
        Must be (num_epochs, 3).

        If empty or missing, no epoching information is available.

        The first and second columns are the start and end index of the epoch.
        The third column is the trigger sample index

        Note that these indices are python-style, i.e. 0-indexed and the last
        point is exclusive.  i.e. (0, 100) is 100 slices long consisting of
        slices 0 to 99 inclusive.
        """

        self.group_codes = []
        """
        Optional list of additional values for each epoch
        """

        self.response_codes = []
        """
        Optional list of response values for each epoch
        """

    def __eq__(self, other):
        if self.channel_ids != other.channel_ids:
            return False

        if self.trigger_codes != other.trigger_codes:
            return False

        if self.trigger_labels != other.trigger_labels:
            return False

        if (self.sample_indexes != other.sample_indexes).any():
            return False

        if self.group_codes != other.group_codes:
            return False

        if self.response_codes != other.response_codes:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def num_epochs(self):
        return self.sample_indexes.shape[0]


    def sanity_check(self):
        if len(self.sample_indexes.shape) != 2:
            raise ValueError("Sample indexes array must be 2D")

        num_epochs = self.sample_indexes.shape[0]

        if len(trigger_codes) != num_epochs:
            raise ValueError("Trigger codes must have same num_epochs as sample_indexes")

        if len(trigger_labels) != 0:
            if len(trigger_labels) != num_epochs:
                raise ValueError("Trigger labels must have 0 or same num_epochs as sample_indexes")

        if len(group_codes) != 0:
            if len(group_codes) != num_epochs:
                raise ValueError("Group codes must have 0 or same num_epochs as sample_indexes")

        if len(response_codes) != 0:
            if len(response_codes) != num_epochs:
                raise ValueError("Response codes must have 0 or same num_epochs as sample_indexes")


    def to_hdf5(self, subgroup):
        # Check that our channel IDs and codes are the appropriate type
        cids = [str(x) for x in self.channel_ids]
        tcs = [str(x) for x in self.trigger_codes]
        tls = [str(x) for x in self.trigger_labels]
        gcs = [str(x) for x in self.group_codes]
        rcs = [str(x) for x in self.response_codes]

        create_subgroup_string_list(subgroup, 'channel_ids', cids)
        create_subgroup_string_list(subgroup, 'trigger_codes', tcs)
        subgroup.create_dataset('sample_indexes', data=self.sample_indexes)

        if len(self.trigger_labels) > 0:
            create_subgroup_string_list(subgroup, 'trigger_labels', tls)

        if len(self.group_codes) > 0:
            create_subgroup_string_list(subgroup, 'group_codes', gcs)

        if len(self.response_codes) > 0:
            create_subgroup_string_list(subgroup, 'response_codes', rcs)

        return subgroup

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        ret.channel_ids = [str(x) for x in subgroup['channel_ids']]
        ret.trigger_codes = [str(x) for x in subgroup['trigger_codes']]
        ret.sample_indexes = subgroup['sample_indexes'][...]

        if 'trigger_labels' in list(subgroup.keys()):
            ret.trigger_labels = [str(x) for x in subgroup['trigger_labels']]

        if 'group_codes' in list(subgroup.keys()):
            ret.group_codes = [str(x) for x in subgroup['group_codes']]

        if 'response_codes' in list(subgroup.keys()):
            ret.response_codes = [str(x) for x in subgroup['response_codes']]

        return ret

    @classmethod
    def from_bti_pdf(cls, bti_pdf):
        ret = cls()

        # Only import epochs if we have more than one
        # BTI always stored one epoch even if it makes no sense
        # Also, BTI epochs are always continuous in the file
        num_epochs = len(bti_pdf.epochs)

        ret.channel_ids = ['TRIGGER'] * num_epochs
        ret.sample_indexes = np.zeros((num_epochs, 3), np.uint64)
        ret.trigger_codes  = [''] * num_epochs
        pt = 0
        for e in range(num_epochs):
            ret.sample_indexes[e, 0] = pt
            # Store the trigger as being at the start point
            ret.sample_indexes[e, 2] = pt

            # Calculate the next start point, i.e. this end point
            pt += bti_pdf.epochs[e].pts_in_epoch
            ret.sample_indexes[e, 1] = pt

            # In epoch mode, we have no record in the PDF of what
            # the triggering event was (as far as I can see)

            # Instead, we just stick in a fake code
            ret.trigger_codes[e] = '1'

        return ret

############################################################################
# Main MEG HDF object
############################################################################

class HDF5Meg(object):
    """
    This class encapsulates the contents of the HDF5MEG format.
    """
    def __init__(self):
        # Metadata attributes to allow for compatibility across versions
        self.format_version = 'rev6'
        """
        The version of the MEGHDF5 format employed in the file
        """

        # XXX: Argue with Nat to remove this (think of matlab etc)
        self.hdf5_version = h5py.version.hdf5_version
        """
        The version of HDF5 used to generate this file
        """

        self.h5py_version = h5py.version.version
        """
        The version of the h5py library used to generate this file
        """

        # Groups
        self.config = HMEGSystemConfig()

        self.geometry = {}
        """
        Dictionary of geometry entries.

        Currently accepted keys are:
            * coils:      HMEGGeomCoils object (mandatory)
            * eeg:        HMEGGeomEEG object
            * fiducials:  HMEGGeomFiducials object (mandatory)
            * head_shape: HMEGGeomHeadshape object
        """

        self.subject = HMEGSubjectData()

        self.acquisitions = HMEGAcquisitions()
        """
        List of data run objects (HMEGAcquisitions)
        """

        self._fileref = None
        """
        Internal file reference which is used to allow destructor
        to close the file when the object goes away
        """

        # NB: We currently don't implement:
        #  * apps
        #  * notes

    def __deepcopy__(self, memo):
        from copy import deepcopy
        # We can just deepcopy most of this
        new = self.__class__()
        new.format_version = deepcopy(self.format_version, memo)
        new.hdf5_version = deepcopy(self.hdf5_version, memo)
        new.h5py_version = deepcopy(self.h5py_version, memo)
        new.config = deepcopy(self.config, memo)
        new.geometry = deepcopy(self.geometry, memo)
        new.subject = deepcopy(self.subject, memo)
        new.acquisitions = deepcopy(self.acquisitions, memo)
        # The file reference just has to be shallow copied across
        new._fileref = self._fileref

        return new

    def __eq__(self, other):
        if self.format_version != other.format_version:
            return False

        if self.hdf5_version != other.hdf5_version:
            return False

        if self.h5py_version != other.h5py_version:
            return False

        if self.config != other.config:
            return False

        if sorted(self.geometry.keys()) != sorted(other.geometry.keys()):
            return False

        for g in list(self.geometry.keys()):
            if self.geometry[g] != other.geometry[g]:
                return False

        if self.subject != other.subject:
            return False

        if self.acquisitions != other.acquisitions:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __del__(self):
        if self._fileref is not None:
            self._fileref.close()

    def sanity_check_all(self):
        """
        Run sanity checks on the whole tree of objects
        """
        # Top level object, i.e. us
        self.sanity_check()

        # Config
        self.config.sanity_check()

        # Each part of geometry
        for g in list(self.geometry.keys()):
            self.geometry[g].sanity_check()

        # Runs
        for r in self.runs:
            r.sanity_check()

    def sanity_check(self):
        # TODO: Sanity check version attributes

        # Check that all channels referenced by runs are known about in the
        # system configuration
        for acq_key, acq in list(self.acquisitions.items()):
            for channel_name in acq.channel_list:
                if channel_name not in list(self.config.channels.keys()):
                    raise Exception("Acquitision %s contains channel %s not in system configuration" % (acq_key, channel_name))

    def to_hdf5(self, subgroup, compress=False):
        """
        The overall MEGHDF5 file format has 6 entries:
            * config
            * geometry
            * acquisitions
            * subject
            * apps
            * notes
        """

        # Local attributes
        subgroup.attrs['format_version'] = ustr(self.format_version)
        subgroup.attrs['hdf5_version'] = ustr(self.hdf5_version)
        subgroup.attrs['h5py_version'] = ustr(self.h5py_version)

        ## config
        self.config.to_hdf5(subgroup.create_group('config'))

        ## geometry
        geom = subgroup.create_group('geometry')
        for gname, ggrp in self.geometry.items():
            ggrp.to_hdf5(geom.create_group(gname))

        ## subject
        self.subject.to_hdf5(subgroup.create_group('subject'))

        ## acquisitions
        self.acquisitions.to_hdf5(subgroup.create_group('acquisitions'), compress)

        return subgroup

    def to_hdf5file(self, filename):
        f = h5py.File(filename, 'w')
        self.to_hdf5(f)
        f.close()

    @classmethod
    def from_hdf5(cls, subgroup):
        ret = cls()

        ## Backwards-incompatibility hack
        if 'data' in list(subgroup.keys()):
            raise Exception('Old alpha-MEGHDF5 file format detected (data).  Aborting..')
        if 'metadata' in list(subgroup.keys()):
            raise Exception('Old alpha-MEGHDF5 file format detected (metadata).  Aborting..')

        # Get our format attributes
        ret.format_version = str(subgroup.attrs.get('format_version', ''))
        ret.hdf5_version   = str(subgroup.attrs.get('hdf5_version', ''))
        ret.h5py_version   = str(subgroup.attrs.get('h5py_version', ''))

        ## config
        if 'config' in list(subgroup.keys()):
            ret.config = HMEGSystemConfig.from_hdf5(subgroup['config'])

        ## geometry
        if 'geometry' in list(subgroup.keys()):
            for geomname, ggrp in subgroup['geometry'].iteritems():
                if geomname == 'fiducials':
                    ret.geometry[geomname] = HMEGGeomFiducials.from_hdf5(ggrp)
                elif geomname == 'eeg':
                    ret.geometry[geomname] = HMEGGeomEEG.from_hdf5(ggrp)
                elif geomname == 'coils':
                    ret.geometry[geomname] = HMEGGeomCoils.from_hdf5(ggrp)
                elif geomname == 'head_shape':
                    ret.geometry[geomname] = HMEGGeomHeadshape.from_hdf5(ggrp)
                else:
                    raise ValueError("Don't understand group %s in geometry" % geomname)

        ## runs
        if 'acquisitions' in list(subgroup.keys()):
            ret.acquisitions = HMEGAcquisitions.from_hdf5(subgroup['acquisitions'])

        # TODO: Implement the apps / notes section when needed

        return ret

    @classmethod
    def from_hdf5file(cls, filename):
        f = h5py.File(filename, 'r')
        ret = cls.from_hdf5(f)
        ret._fileref = f
        return ret

__all__.append('HDF5Meg')

def bti_to_meghdf_data(bti_config, runs, run_codes, default_index = None,
                       bti_hs = None, subject_identifier = "",
                       applyupb = False):
    """
    :param bti_config: BTIConfig object
    :param runs: List of BTIPDF objects to import
    :param run_codes: List of run type strings, one per entry in run
    :param default_index: Integer referencing the main run
    :param bti_hsfile: BTIHSfile object
    :param subject_identifier: Subject identifier for run (string)
    :param applyupb: Convert to float and apply UPB

    :rtype: HDF5Meg
    """
    if len(runs) != len(run_codes):
        raise Exception('Need one run code per run')

    if (default_index is not None) and (default_index >= len(runs)):
        raise Exception('Default index must index into runs list')

    h = HDF5Meg()

    # Create the metadata information
    # With BTI files, we can only at best have the subject ID
    h.subject.subject_id = subject_identifier

    # Create the config information
    h.config = HMEGSystemConfig.from_bti_config(bti_config)

    if 'digital' in h.config.weights_tables:
        # We assume that the digital weights are applied as this was nearly
        # always done by the 4D system
        weights_configured = 'digital'
        weights_applied = 'digital'
    else:
        weights_configured = ''
        weights_applied = ''


    # This is a YNiC Specific hack
    if h.config.location == 'YNiC':
        # Deal with A203 having the wrong loop radius in older data files
        if 'A203' in h.config.channels:
            a203 = h.config.channels['A203']
            if a203.loop_radius == 0.015:
                # Should be 0.009
                print("YNiC: Fixing A203 radius in older file to 0.009")
                a203.loop_radius = np.array([0.009])

    # We now need to scan each run and check for any channel aliases which
    # need to be added
    for run in runs:
        for pdfchan in run.channels:
            # Remember that chan_no in the PDF is 1-indexed (!)
            chan_no = pdfchan.chan_no - 1

            # Remove any -1 on the end (this seems to be artefactual)
            chan_label = pdfchan.chan_label
            if chan_label.endswith('-1'):
                chan_label = chan_label[:-2]

            # Look up the "real" channel and check if this is an alias
            config_chan = bti_config.channels[chan_no]

            if chan_label != config_chan.hdr.name:
                # Check that we don't already have this as an alias
                hchan = h.config.channels[config_chan.hdr.name]

                if chan_label not in hchan.aliases:
                    hchan.aliases.append(chan_label)

    # Create the different pieces of geometry information
    fidu = HMEGGeomFiducials.from_bti_config(bti_config)
    if fidu is not None:
        h.geometry['fiducials'] = fidu

    coils = HMEGGeomCoils.from_bti_config(bti_config)
    if coils is not None:
        h.geometry['coils'] = coils

    eeg = HMEGGeomEEG.from_bti_config(bti_config)
    if eeg is not None:
        h.geometry['eeg'] = eeg

    if bti_hs is not None:
        h.geometry['head_shape'] = HMEGGeomHeadshape.from_bti_hsfile(bti_hs)

    # Find the ccs to scs transform
    # Note: Do not use b_ccp_xfm_block as this is corrupt in certain files
    ccs_to_scs = bti_config.transforms[0]

    # Need to ensure that last row is [0, 0, 0, 1]
    # as the 4D software does not write it out correctly
    ccs_to_scs[3, :] = [0, 0, 0, 1.0]

    # We have to take into account our shift to mm in the translation
    ccs_to_scs[0:3, 3] *= 1000.0

    # and then we have to modify the transformation to take into account our
    # ALS -> RAS switch
    premul = np.array([[0, -1, 0, 0],
                       [1, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

    postmul = np.array([[0, 1, 0, 0],
                        [-1, 0, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1.0]])

    ccs_to_scs = premul.dot(ccs_to_scs.dot(postmul))

    for run_num in range(len(runs)):
        # Give runs simple names
        acq = HMEGAcquisition.from_bti_pdf( runs[run_num],
                                            bti_config,
                                            run_num,
                                            run_codes[run_num],
                                            applyupb)

        # Make sure that we note that our weights have been applied
        acq.weights_configured = weights_configured
        acq.weights_applied = weights_applied

        # For main acquisition runs, attach the ccs_to_scs object
        if run_codes[run_num] == 'ACQ':
            acq.ccs_to_scs_transform = ccs_to_scs

        h.acquisitions.acquisitions[str(run_num)] = acq

        if default_index == run_num:
            h.acquisitions.default_acq_name = str(run_num)

    return h

__all__.append('bti_to_meghdf_data')
