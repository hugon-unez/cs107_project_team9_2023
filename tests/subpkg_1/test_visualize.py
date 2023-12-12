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

        with pytest.raises(TypeError, match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."):
            visualizer = SpectralVisualizer(row=row_data, data=data)

    def test_visualizer_with_invalid_row_type(self):
        # Attempt to create an instance with an invalid type for row
        invalid_row = {'plate': np.array([15150]), 'mjd': np.array([59291]), 'fiberid': np.array([1, 2])}

        with pytest.raises(TypeError, match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."):
            visualizer = SpectralVisualizer(row=invalid_row)

    def test_visualizer_with_invalid_data_type(self):
        # Attempt to create an instance with an invalid type for data
        invalid_data = pd.Series({'Wavelength': [1, 2, 3], 'Flux': [0.5, 0.8, 1.0]})

        with pytest.raises(TypeError, match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."):
            visualizer = SpectralVisualizer(data=invalid_data)

