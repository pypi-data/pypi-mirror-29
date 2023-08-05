# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour.colorimetry.lightness` module.
"""

from __future__ import division, unicode_literals

import numpy as np
import unittest

from colour.colorimetry import (lightness_Glasser1958, lightness_Wyszecki1963,
                                lightness_CIE1976, lightness_Fairchild2010,
                                lightness_Fairchild2011)
from colour.utilities import ignore_numpy_errors

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'TestLightnessGlasser1958', 'TestLightnessWyszecki1963',
    'TestLightnessCIE1976', 'TestLightnessFairchild2010',
    'TestLightnessFairchild2011'
]


class TestLightnessGlasser1958(unittest.TestCase):
    """
    Defines :func:`colour.colorimetry.lightness.lightness_Glasser1958`
    definition unit tests methods.
    """

    def test_lightness_Glasser1958(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Glasser1958`
        definition.
        """

        self.assertAlmostEqual(
            lightness_Glasser1958(10.08), 36.25056265, places=7)

        self.assertAlmostEqual(
            lightness_Glasser1958(56.76), 78.81179990, places=7)

        self.assertAlmostEqual(
            lightness_Glasser1958(98.32), 98.34470526, places=7)

    def test_n_dimensional_lightness_Glasser1958(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Glasser1958`
        definition n-dimensional arrays support.
        """

        Y = 10.08
        L = 36.25056265
        np.testing.assert_almost_equal(lightness_Glasser1958(Y), L, decimal=7)

        Y = np.tile(Y, 6)
        L = np.tile(L, 6)
        np.testing.assert_almost_equal(lightness_Glasser1958(Y), L, decimal=7)

        Y = np.reshape(Y, (2, 3))
        L = np.reshape(L, (2, 3))
        np.testing.assert_almost_equal(lightness_Glasser1958(Y), L, decimal=7)

        Y = np.reshape(Y, (2, 3, 1))
        L = np.reshape(L, (2, 3, 1))
        np.testing.assert_almost_equal(lightness_Glasser1958(Y), L, decimal=7)

    @ignore_numpy_errors
    def test_nan_lightness_Glasser1958(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Glasser1958`
        definition nan support.
        """

        lightness_Glasser1958(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]))


class TestLightnessWyszecki1963(unittest.TestCase):
    """
    Defines :func:`colour.colorimetry.lightness.lightness_Wyszecki1963`
    definition unit tests methods.
    """

    def test_lightness_Wyszecki1963(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Wyszecki1963`
        definition.
        """

        self.assertAlmostEqual(
            lightness_Wyszecki1963(10.08), 37.00411491, places=7)

        self.assertAlmostEqual(
            lightness_Wyszecki1963(56.76), 79.07730319, places=7)

        self.assertAlmostEqual(
            lightness_Wyszecki1963(98.32), 98.38622505, places=7)

    def test_n_dimensional_lightness_Wyszecki1963(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Wyszecki1963`
        definition n-dimensional arrays support.
        """

        Y = 10.08
        W = 37.004114912764535
        np.testing.assert_almost_equal(lightness_Wyszecki1963(Y), W, decimal=7)

        Y = np.tile(Y, 6)
        W = np.tile(W, 6)
        np.testing.assert_almost_equal(lightness_Wyszecki1963(Y), W, decimal=7)

        Y = np.reshape(Y, (2, 3))
        W = np.reshape(W, (2, 3))
        np.testing.assert_almost_equal(lightness_Wyszecki1963(Y), W, decimal=7)

        Y = np.reshape(Y, (2, 3, 1))
        W = np.reshape(W, (2, 3, 1))
        np.testing.assert_almost_equal(lightness_Wyszecki1963(Y), W, decimal=7)

    @ignore_numpy_errors
    def test_nan_lightness_Wyszecki1963(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Wyszecki1963`
        definition nan support.
        """

        lightness_Wyszecki1963(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]))


class TestLightnessCIE1976(unittest.TestCase):
    """
    Defines :func:`colour.colorimetry.lightness.lightness_CIE1976` definition
    unit tests methods.
    """

    def test_lightness_CIE1976(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_CIE1976`
        definition.
        """

        self.assertAlmostEqual(lightness_CIE1976(10.08), 37.98562910, places=7)

        self.assertAlmostEqual(lightness_CIE1976(56.76), 80.04441556, places=7)

        self.assertAlmostEqual(lightness_CIE1976(98.32), 99.34672790, places=7)

        self.assertAlmostEqual(
            lightness_CIE1976(10.08, 50), 52.01763049, places=7)

        self.assertAlmostEqual(
            lightness_CIE1976(10.08, 75), 43.41887326, places=7)

        self.assertAlmostEqual(
            lightness_CIE1976(10.08, 95), 38.91659876, places=7)

    def test_n_dimensional_lightness_CIE1976(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_CIE1976`
        definition n-dimensional arrays support.
        """

        Y = 10.08
        Lstar = 37.98562910
        np.testing.assert_almost_equal(lightness_CIE1976(Y), Lstar, decimal=7)

        Y = np.tile(Y, 6)
        Lstar = np.tile(Lstar, 6)
        np.testing.assert_almost_equal(lightness_CIE1976(Y), Lstar, decimal=7)

        Y = np.reshape(Y, (2, 3))
        Lstar = np.reshape(Lstar, (2, 3))
        np.testing.assert_almost_equal(lightness_CIE1976(Y), Lstar, decimal=7)

        Y = np.reshape(Y, (2, 3, 1))
        Lstar = np.reshape(Lstar, (2, 3, 1))
        np.testing.assert_almost_equal(lightness_CIE1976(Y), Lstar, decimal=7)

    @ignore_numpy_errors
    def test_nan_lightness_CIE1976(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_CIE1976`
        definition nan support.
        """

        lightness_CIE1976(np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]))


class TestLightnessFairchild2010(unittest.TestCase):
    """
    Defines :func:`colour.colorimetry.lightness.lightness_Fairchild2010`
    definition unit tests methods.
    """

    def test_lightness_Fairchild2010(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Fairchild2010`
        definition.
        """

        self.assertAlmostEqual(
            lightness_Fairchild2010(10.08 / 100), 24.90229027, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2010(56.76 / 100), 88.79756887, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2010(98.32 / 100), 95.61301852, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2010(10.08 / 100, 2.75), 16.06420271, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2010(1008), 100.019986327374240, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2010(100800), 100.019999997090270, places=7)

    def test_n_dimensional_lightness_Fairchild2010(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Fairchild2010`
        definition n-dimensional arrays support.
        """

        Y = 10.08 / 100
        L = 24.90229027
        np.testing.assert_almost_equal(
            lightness_Fairchild2010(Y), L, decimal=7)

        Y = np.tile(Y, 6)
        L = np.tile(L, 6)
        np.testing.assert_almost_equal(
            lightness_Fairchild2010(Y), L, decimal=7)

        Y = np.reshape(Y, (2, 3))
        L = np.reshape(L, (2, 3))
        np.testing.assert_almost_equal(
            lightness_Fairchild2010(Y), L, decimal=7)

        Y = np.reshape(Y, (2, 3, 1))
        L = np.reshape(L, (2, 3, 1))
        np.testing.assert_almost_equal(
            lightness_Fairchild2010(Y), L, decimal=7)

    @ignore_numpy_errors
    def test_nan_lightness_Fairchild2010(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Fairchild2010`
        definition nan support.
        """

        lightness_Fairchild2010(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]))


class TestLightnessFairchild2011(unittest.TestCase):
    """
    Defines :func:`colour.colorimetry.lightness.lightness_Fairchild2011`
    definition unit tests methods.
    """

    def test_lightness_Fairchild2011(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Fairchild2011`
        definition.
        """

        self.assertAlmostEqual(
            lightness_Fairchild2011(10.08 / 100), 26.45950982, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2011(56.76 / 100), 71.70846602, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2011(98.32 / 100), 93.03097540, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2011(10.08 / 100, 2.75), 0.08672116, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2011(1008), 244.07716521, places=7)

        self.assertAlmostEqual(
            lightness_Fairchild2011(100800), 246.90681934, places=7)

    def test_n_dimensional_lightness_Fairchild2011(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Fairchild2011`
        definition n-dimensional arrays support.
        """

        Y = 10.08 / 100
        L = 26.45950982
        np.testing.assert_almost_equal(
            lightness_Fairchild2011(Y), L, decimal=7)

        Y = np.tile(Y, 6)
        L = np.tile(L, 6)
        np.testing.assert_almost_equal(
            lightness_Fairchild2011(Y), L, decimal=7)

        Y = np.reshape(Y, (2, 3))
        L = np.reshape(L, (2, 3))
        np.testing.assert_almost_equal(
            lightness_Fairchild2011(Y), L, decimal=7)

        Y = np.reshape(Y, (2, 3, 1))
        L = np.reshape(L, (2, 3, 1))
        np.testing.assert_almost_equal(
            lightness_Fairchild2011(Y), L, decimal=7)

    @ignore_numpy_errors
    def test_nan_lightness_Fairchild2011(self):
        """
        Tests :func:`colour.colorimetry.lightness.lightness_Fairchild2011`
        definition nan support.
        """

        lightness_Fairchild2011(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]))


if __name__ == '__main__':
    unittest.main()
