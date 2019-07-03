"""
This test module has tests relating to mesoporous pore size calculations.

All functions in /calculations/psd_mesoporous.py are tested here.
The purposes are:

    - testing the user-facing API function (psd_mesoporous)
    - testing individual low level functions against known results.

Functions are tested against pre-calculated values on real isotherms.
It is difficult to store full pore size distributions, therefore the
cumulative pore volume as determined by each method is checked
versus a stored value, with a margin of error.
All pre-calculated data for characterization can be found in
the /.conftest file together with the other isotherm parameters.
"""

import os

import numpy as np
import pytest
from matplotlib.testing.decorators import cleanup

import pygaps
import pygaps.calculations.psd_mesoporous as pmes
from pygaps.utilities.exceptions import ParameterError

from .conftest import DATA
from .conftest import DATA_N77_PATH


@pytest.mark.characterisation
class TestPSDMeso():
    """Test mesopore size distribution calculation."""

    def test_psd_meso_checks(self, basic_pointisotherm):
        """Checks for built-in safeguards."""
        # Will raise a "no model exception"
        with pytest.raises(ParameterError):
            pmes.psd_mesoporous(basic_pointisotherm, psd_model=None)

        # Will raise a "no suitable model exception"
        with pytest.raises(ParameterError):
            pmes.psd_mesoporous(basic_pointisotherm, psd_model='test')

        # Will raise a "no applicable geometry exception"
        with pytest.raises(ParameterError):
            pmes.psd_mesoporous(basic_pointisotherm, pore_geometry='test')

        # Will raise a "no applicable branch exception"
        with pytest.raises(ParameterError):
            pmes.psd_mesoporous(basic_pointisotherm, branch='test')

    @pytest.mark.parametrize('method', [
        'pygaps-DH',
        'BJH',
        'DH',
    ])
    @pytest.mark.parametrize('sample', [
        sample for sample in list(DATA.values())
    ])
    def test_psd_meso(self, sample, method):
        """Test psd calculation with several model isotherms."""
        # exclude datasets where it is not applicable
        if sample.get('psd_meso_pore_size', None):

            filepath = os.path.join(DATA_N77_PATH, sample['file'])

            with open(filepath, 'r') as text_file:
                isotherm = pygaps.isotherm_from_json(text_file.read())

            result_dict = pmes.psd_mesoporous(
                isotherm,
                psd_model=method,
                branch='des')

            loc = np.where(result_dict['pore_distribution'] == max(result_dict['pore_distribution']))
            principal_peak = result_dict['pore_widths'][loc]

            err_relative = 0.05  # 5 percent
            err_absolute = 0.01  # 0.01

            assert np.isclose(
                principal_peak,
                sample['psd_meso_pore_size'],
                err_relative, err_absolute)

    @cleanup
    def test_psd_meso_verbose(self):
        """Test verbosity."""
        data = DATA['MCM-41']
        filepath = os.path.join(DATA_N77_PATH, data['file'])

        with open(filepath, 'r') as text_file:
            isotherm = pygaps.isotherm_from_json(
                text_file.read())

        pygaps.psd_mesoporous(isotherm, verbose=True)
