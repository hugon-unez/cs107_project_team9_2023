import unittest
from unittest.mock import patch
import matplotlib
import matplotlib.pyplot as plt
from astropy.table import Table
import numpy as np
import pandas as pd
import pytest
from group9_package.subpkg_1.visualize_module import SpectralVisualizer

# need to update with more tests

class TestVisualizer():
    def test_visualizer_with_both_row_and_data(self):
        # Attempt to create an instance with both row and data provided, which we do not want
        row_data = {'plate': np.array([15150]), 'mjd': np.array([59291]), 'fiberid': np.array([1])}
        data = pd.DataFrame({'Wavelength': [1, 2, 3], 'Flux': [0.5, 0.8, 1.0]})

        # match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."

        with pytest.raises(TypeError):
            visualizer = SpectralVisualizer(row=row_data, data=data)

    def test_visualizer_with_invalid_row_type(self):
        # Attempt to create an instance with an invalid type for row
        invalid_row = {'plate': np.array([15150]), 'mjd': np.array([59291]), 'fiberid': np.array([1, 2])}
        
        #match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."
        with pytest.raises(TypeError):
            visualizer = SpectralVisualizer(row=invalid_row)

    def test_visualizer_with_invalid_data_type(self):
        # Attempt to create an instance with an invalid type for data
        invalid_data = pd.Series({'Wavelength': [1, 2, 3], 'Flux': [0.5, 0.8, 1.0]})

        # match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."
        with pytest.raises(TypeError):
            visualizer = SpectralVisualizer(data=invalid_data)

    def test_visualizer_with_no_data_or_row(self):
        # Attempt to create an instance with an invalid row and data
        with pytest.raises(ValueError):
            visualizer = SpectralVisualizer(data=None, row=None)

    #test the visualize function raises the appropriate error when data returned is None
    @patch('group9_package.subpkg_1.core_functions_module_extract.SpectraExtract.extract_spectra')
    def test_visualize_with_no_data(self, mock_query_sql):
        # Patch return

        data_row = Table({'plate': np.array([15150]), 'mjd': np.array([59291]), 'fiberid': np.array([1])})

        mock_query_sql.return_value = None

        #pass in correct row type
        visualizer = SpectralVisualizer(row=data_row[0], data=None)

        with pytest.raises(ValueError):
            visualizer.visualize()

    def test_visualize_shows_graph(self):
        matplotlib.use('Agg')
        
        # define sample dataFrame
        data = pd.DataFrame({'Wavelength': [1, 2, 3], 'Flux': [0.5, 0.8, 1.0]})

        visualizer = SpectralVisualizer(row=None, data=data)

         #visualize data and confirm graph shows
        with patch('matplotlib.pyplot.show') as mock_show:
            visualizer.visualize()

        # Check if plt.show() was called
        mock_show.assert_called_once()

        # Reset the backend to the default
        plt.close('all')
        matplotlib.use('TkAgg')
            

