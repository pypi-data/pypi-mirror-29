# -*- coding: utf-8 -*-
"""
ColorMatch RGB Colourspace
==========================

Defines the *ColorMatch RGB* colourspace:

-   :attr:`colour.models.COLOR_MATCH_RGB_COLOURSPACE`.

See Also
--------
`RGB Colourspaces Jupyter Notebook
<http://nbviewer.jupyter.org/github/colour-science/colour-notebooks/\
blob/master/notebooks/models/rgb.ipynb>`_

References
----------
-   :cite:`Lindbloom2014a` : Lindbloom, B. (2014). RGB Working Space
    Information. Retrieved April 11, 2014, from
    http://www.brucelindbloom.com/WorkingSpaceInfo.html
"""

from __future__ import division, unicode_literals

import numpy as np
from functools import partial

from colour.colorimetry import ILLUMINANTS
from colour.models.rgb import (RGB_Colourspace, function_gamma,
                               normalised_primary_matrix)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'COLOR_MATCH_RGB_PRIMARIES', 'COLOR_MATCH_RGB_ILLUMINANT',
    'COLOR_MATCH_RGB_WHITEPOINT', 'COLOR_MATCH_RGB_TO_XYZ_MATRIX',
    'XYZ_TO_COLOR_MATCH_RGB_MATRIX', 'COLOR_MATCH_RGB_COLOURSPACE'
]

COLOR_MATCH_RGB_PRIMARIES = np.array([
    [0.6300, 0.3400],
    [0.2950, 0.6050],
    [0.1500, 0.0750],
])
"""
*ColorMatch RGB* colourspace primaries.

COLOR_MATCH_RGB_PRIMARIES : ndarray, (3, 2)
"""

COLOR_MATCH_RGB_ILLUMINANT = 'D50'
"""
*ColorMatch RGB* colourspace whitepoint name as illuminant.

COLOR_MATCH_RGB_ILLUMINANT : unicode
"""

COLOR_MATCH_RGB_WHITEPOINT = (ILLUMINANTS[
    'CIE 1931 2 Degree Standard Observer'][COLOR_MATCH_RGB_ILLUMINANT])
"""
*ColorMatch RGB* colourspace whitepoint.

COLOR_MATCH_RGB_WHITEPOINT : ndarray
"""

COLOR_MATCH_RGB_TO_XYZ_MATRIX = normalised_primary_matrix(
    COLOR_MATCH_RGB_PRIMARIES, COLOR_MATCH_RGB_WHITEPOINT)
"""
*ColorMatch RGB* colourspace to *CIE XYZ* tristimulus values matrix.

COLOR_MATCH_RGB_TO_XYZ_MATRIX : array_like, (3, 3)
"""

XYZ_TO_COLOR_MATCH_RGB_MATRIX = np.linalg.inv(COLOR_MATCH_RGB_TO_XYZ_MATRIX)
"""
*CIE XYZ* tristimulus values to *ColorMatch RGB* colourspace matrix.

XYZ_TO_COLOR_MATCH_RGB_MATRIX : array_like, (3, 3)
"""

COLOR_MATCH_RGB_COLOURSPACE = RGB_Colourspace(
    'ColorMatch RGB',
    COLOR_MATCH_RGB_PRIMARIES,
    COLOR_MATCH_RGB_WHITEPOINT,
    COLOR_MATCH_RGB_ILLUMINANT,
    COLOR_MATCH_RGB_TO_XYZ_MATRIX,
    XYZ_TO_COLOR_MATCH_RGB_MATRIX,
    partial(function_gamma, exponent=1 / 1.8),
    partial(function_gamma, exponent=1.8), )
COLOR_MATCH_RGB_COLOURSPACE.__doc__ = """
*ColorMatch RGB* colourspace.

References
----------
-   :cite:`Lindbloom2014a`

COLOR_MATCH_RGB_COLOURSPACE : RGB_Colourspace
"""
