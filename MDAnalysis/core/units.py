# -*- coding: utf-8 -*-

# Copyright (c) 2009 Oliver Beckstein <orbeckst@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Constants and unit conversion
=============================

The base units of MDAnalysis are *Angstrom* for *length* (1 Angstrom =
0.1 nm = 10^-10 m) and *ps* (pico second) for *time* (1 ps = 10^-12
sec).

All conversions: the conversion factor f to a unit b' for a quantity X
(whose numeric value relative to the base unit b is stored in the
program) is a quantity with unit b'/b. In the dictionaries below only
the numeric value f(b->b') is stored.

  X/b' = f(b->b') * X/b

:func:`get_conversion_factor` returns the appropriate factor f(b->b').

Conversion is done via the base units::

    x is in u1: from u1 to b:  x'  = x  / factor[u1]
                from b  to u2: x'' = x' * factor[u2]
    so f[u1,u2] = factor[u2]/factor[u1]


Conversions
-----------

density conversion factor. Base unit is A**-3

   n/x = n/A**3 * densityUnit_factor[x]

nm:

   f = 1 A^-3/1 nm^-3 = 1/(10A)^-3 = 1/1000

Molar:

   factor = 1 A**-3 / (N_Avogadro * (10**-9 dm)**-3)

relative to a density rho0 in g/cm^3:

    M(H2O) = 18 g/mol   Molar mass of water

    factor = 1/(1e-24 * N_Avogadro / M(H2O))

from rho/rho0 = n/(N_A * M**-1) / rho0  where [n] = 1/Volume, [rho] = mass/Volume


.. SeeAlso:: Maybe we should simply use Quantities_ instead of this
             home grown attempt?

.. _Quantities: http://packages.python.org/quantities/
"""

#: conversion factors between the base unit (Angstrom) and other lengthUnits x:
#: L/x = L/A * lengthUnit_factor[x]
lengthUnit_factor = {'Angstrom': 1.0, 'A': 1.0, 'Å': 1.0,
                     'nm': 1.0/10, 'nanometer': 1.0/10,
                     }


#: Avogadro's constant in mol**-1, from http://physics.nist.gov/cgi-bin/cuu/Value?na
N_Avogadro = 6.02214179e+23  # mol**-1   


#: water density: Jorgensen & Jenson, JCompChem 19 (1998), 1179: T=298K, P=1atm
#:  ======== =========
#:  model    g cm**-3
#:  ======== =========
#:    SPC     0.985(1)
#:    TIP3P   1.002(1)
#:    TIP4P   1.001(1)
#:    exp     0.997
#:  ======== =========
#: and molar mass 18.016 g mol**-1.
water = {'exp':0.997, 'SPC':0.985, 'TIP3P':1.002, 'TIP4P':1.001,  # in g cm**-3
         'MolarMass': 18.016,                                     # in g mol**-1
         }

#: for water densities, this is the volume per water molecule in A**3
densityUnit_factor = {
    'Angstrom^{-3}': 1/1.0, 'A^{-3}': 1/1.0, 'Å^{-3}': 1/1.0, 
    'nm^{-3}': 1/1e-3, 'nanometer^{-3}': 1/1e-3,
    'Molar': 1/(1e-27*N_Avogadro),
    'SPC':   1/(1e-24*N_Avogadro*water['SPC']  / water['MolarMass']),
    'TIP3P': 1/(1e-24*N_Avogadro*water['TIP3P']/ water['MolarMass']),
    'TIP4P': 1/(1e-24*N_Avogadro*water['TIP4P']/ water['MolarMass']),
    'water': 1/(1e-24*N_Avogadro*water['exp']  / water['MolarMass']),
    }


#: basic unit is ps
#: 1 AKMA time unit = 4.888821E-14 sec
#: http://www.charmm.org/html/documentation/c35b1/usage.html#%20AKMA
#: 1200ps/ps * f = 1.2 ns/ns  ==> f = 1/1000
timeUnit_factor = {'ps': 1/1.0,
                   'ns': 1/1e3,
                   'second': 1/1e12,
                   'AKMA': 1/4.888821e-2,
                   }

#: :data:`conversion_factor` is used by :func:`get_conversion_factor`:
#:
#: Note: any observable with a unit (i.e. one with an entry in
# the :attr:`unit` attribute) needs an entry in :data:`conversion_factor`
conversion_factor = {'length': lengthUnit_factor,
                     'density': densityUnit_factor,
                     'time': timeUnit_factor,
                     }

#: Generated lookup table (dict): returns the type of unit for a known input unit.
unit_types = {}
for utype,ufactor in conversion_factor.items():
    for unit in ufactor.keys():
        unit_types[unit] = utype


def get_conversion_factor(unit_type,u1,u2):
    """generate the conversion factor u1 -> u2 by using the base unit as an intermediate

    f[u1 -> u2] = factor[u2]/factor[u1]

    Conversion of X (in u1) to X' (in u2):

        X' = conversion_factor * X
    """
    # x is in u1: from u1 to b:  x'  = x  / factor[u1]
    #             from b  to u2: x'' = x' * factor[u2]
    # so f[u1,u2] = factor[u2]/factor[u1]
    return conversion_factor[unit_type][u2] / conversion_factor[unit_type][u1]

def convert(x, u1, u2):
    """Convert value in unit *u1* to *u2*."""
    try:
        ut1 = unit_types[u1]
        ut2 = unit_types[u2]
    except KeyError:
        raise ValueError("units must be one of %r, not %r or %r" % 
                         (unit_types.keys(), u1, u2))
    if ut1 != ut2:
        raise ValueError("Cannot convert between unit types %(ut1)s --> %(ut2)s" %
                         vars())
    return x * get_conversion_factor(ut1, u1, u2)
 
    