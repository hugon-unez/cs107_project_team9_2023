import matplotlib as plt
from astropy.table import Table
import numpy as np
from group9_package.subpkg_1.visualize_module import SpectralVisualizer


def test_visualizer_plot():
   # Create an instance of SpectralVisualizer with a fake row based on sdss docs
   row_data = {'plate': np.array([15150]), 'mjd': np.array([59291]), 'fiberid': np.array([1])}
   table = Table(row_data, names=('plate', 'mjd', 'fiberid'))


   # Access the row in the table
   row = table[0]


   # Execute SpectralVisualizer
   visualizer = SpectralVisualizer(row=row)


   # Call the visualize method
   visualizer.visualize()


   # Access the current figure
   fig = plt.gcf()


   # Assert on the attributes of the plot
   assert len(fig.axes) == 1, "Expected a single subplot"