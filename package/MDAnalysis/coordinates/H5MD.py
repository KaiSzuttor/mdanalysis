# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDAnalysis --- http://www.MDAnalysis.org
# Copyright (c) 2006-2015 Naveen Michaud-Agrawal, Elizabeth J. Denning, Oliver Beckstein
# and contributors (see AUTHORS for the full list)
#
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.
# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.
# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787
#

"""
H5MD file format --- :mod:`MDAnalysis.coordinates.H5MD`
======================================================

Class to read H5MD coordinate files.

"""

import h5py

from . import base


class Timestep(base.Timestep):
    pass


class H5MDReader(base.Reader):
    format = ['h5', 'h5md']
    units = {'time': 'ps', 'length': 'Angstrom'}
    _Timestep = Timestep

    def __init__(self, filename, n_atoms=None, **kwargs):
        super(H5MDReader, self).__init__(filename, **kwargs)
        self._n_atoms = n_atoms
        self._n_frames = None
        self.trjfile = None  # have _read_next_timestep() open it properly!
        self.ts = self._Timestep(self.n_atoms, **self._ts_kwargs)
        try:
            self.h5mdfile = h5py.File(filename, 'r')
        except:
            raise IOError("Could not open h5md file.")

    def _read_next_timestep(self, ts=None):  # pragma: no cover
        # Example from DCDReader:
         if ts is None:
             ts = self.ts
         ts.frame = self._read_next_frame(etc)
         return ts

    def _read_frame(self, frame):
        """Move to *frame* and fill timestep with data."""
        raise TypeError("{0} does not support direct frame indexing."
                        "".format(self.__class__.__name__))
        # Example implementation in the DCDReader:
        # self._jump_to_frame(frame)
        # ts = self.ts
        # ts.frame = self._read_next_frame(ts._x, ts._y, ts._z, ts._unitcell, 1)
        # return ts
