import matplotlib as plt
from astropy.table import Table
import numpy as np
import pandas as pd
import pytest
from group9_package.subpkg_1.visualize_module import SpectralVisualizer

def test_visualizer_with_both_row_and_data():
    # Attempt to create an instance with both row and data provided, which we do not want
    row_data = {'plate': np.array([15150]), 'mjd': np.array([59291]), 'fiberid': np.array([1])}
    data = pd.DataFrame({'Wavelength': [1, 2, 3], 'Flux': [0.5, 0.8, 1.0]})

    with pytest.raises(ValueError, match="Either 'row' or 'data' should be provided, but not both or neither."):
        visualizer = SpectralVisualizer(row=row_data, data=data)

def test_visualizer_with_invalid_row_type():
    # Attempt to create an instance with an invalid row type
    with pytest.raises(TypeError, match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."):
        visualizer = SpectralVisualizer(row="invalid_row_type")

def test_visualizer_plot():
    # Create an instance of SpectralVisualizer with a fake row based on sdss docs
    row_data = {'plate': np.array([15150]), 'mjd': np.array([59291]), 'fiberid': np.array([1])}
    table = Table(row_data, names=('plate', 'mjd', 'fiberid'))


    # Access the row in the table
    row = table[0]


   # Execute SpectralVisualizer
    visualizer = SpectralVisualizer(row=row)

   # Test for empty data
    with pytest.raises(ValueError, match="Both 'data' and 'row' are None or empty. Provide either 'data' or 'row' with valid data."):
        visualizer.visualize()


    # Call the visualize method
    visualizer.visualize()


    # Access the current figure
    fig = plt.gcf()


    # Assert on the attributes of the plot
    assert len(fig.axes) == 1, "Expected a single subplot"
