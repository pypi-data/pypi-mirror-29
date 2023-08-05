# -*- coding: utf-8 -*-
"""
Showcases deprecated colour models computations.
"""

import numpy as np

import colour
from colour.utilities import message_box

message_box(('Deprecated Colour Models Computations\n'
             '\nDon\'t use that! Seriously...'))

RGB = np.array([0.49019608, 0.98039216, 0.25098039])
message_box(('Converting to "HSV" colourspace from given "RGB" colourspace '
             'values:\n'
             '\n\t{0}'.format(RGB)))
print(colour.RGB_to_HSV(RGB))

print('\n')

HSV = np.array([0.27867384, 0.74400000, 0.98039216])
message_box(('Converting to "RGB" colourspace from given "HSV" colourspace '
             'values:\n'
             '\n\t{0}'.format(HSV)))
print(colour.HSV_to_RGB(HSV))

print('\n')

message_box(('Converting to "HSL" colourspace from given "RGB" colourspace '
             'values:\n'
             '\n\t{0}'.format(RGB)))
print(colour.RGB_to_HSL(RGB))

print('\n')

HSL = np.array([0.27867384, 0.94897959, 0.61568627])
message_box(('Converting to "RGB" colourspace from given "HSL" colourspace '
             'values:\n'
             '\n\t{0}'.format(HSL)))
print(colour.HSL_to_RGB(HSL))

print('\n')

message_box(('Converting to "CMY" colourspace from given "RGB" colourspace '
             'values:\n'
             '\n\t{0}'.format(RGB)))
print(colour.RGB_to_CMY(RGB))

print('\n')

CMY = np.array([0.50980392, 0.01960784, 0.74901961])
message_box(('Converting to "RGB" colourspace from given "CMY" colourspace '
             'values:\n'
             '\n\t{0}'.format(CMY)))
print(colour.CMY_to_RGB(CMY))

print('\n')

message_box(('Converting to "CMYK" colourspace from given "CMY" colourspace '
             'values:\n'
             '\n\t{0}'.format(CMY)))
print(colour.CMY_to_CMYK(CMY))

print('\n')

CMYK = np.array([0.50000000, 0.00000000, 0.74400000, 0.01960784])
message_box(('Converting to "CMY" colourspace from given "CMYK" colourspace '
             'values:\n'
             '\n\t{0}'.format(CMYK)))
print(colour.CMYK_to_CMY(CMYK))
