# -*- coding: utf-8 -*-
"""
Showcases *Rayleigh Optical Depth* computations examples.
"""

import colour
from colour.utilities import message_box

message_box('"Rayleigh" Optical Depth Computations')

message_box(('Creating a "Rayleigh" spectral power distribution with default '
             'spectral shape:\n'
             '\n\t{0}'.format(colour.DEFAULT_SPECTRAL_SHAPE)))
spd = colour.rayleigh_scattering_spd()
print(spd[555])

print('\n')

wavelength = 555 * 10e-8
message_box(('Computing the scattering cross section per molecule at given '
             'wavelength in cm:\n'
             '\n\tWavelength: {0} cm'.format(wavelength)))
print(colour.phenomena.scattering_cross_section(wavelength))

print('\n')

message_box(('Computing the "Rayleigh" optical depth as function of '
             'wavelength in cm:\n'
             '\n\tWavelength: {0} cm'.format(wavelength)))
print(colour.phenomena.rayleigh_optical_depth(wavelength))
