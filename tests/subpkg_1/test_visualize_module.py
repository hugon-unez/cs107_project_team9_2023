"""
This integration test module runs tests for visualize_module.py.
Specifically, it ensures that the module works with the core_functions_module_extract
"""

import pytest
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from unittest.mock import patch
from astropy.table import Table
from group9_package.subpkg_1.visualize_module import SpectralVisualizer
from group9_package.subpkg_1.core_functions_module_extract import SpectraExtract, SpectralAnalysisBase

class TestVisualizer():
    """A class for testing our methods in the SpectralVisualizer Class"""
    @pytest.fixture
    def setup_visualizer(self):
        """
        Define pytest valid_data_row, invalid_data_row_incorrect_type, 
        invalid_data_row_missing_column, spectra_data_valid, spectra_data_incorrect_type
        """
        # Define a sample ADQL query to obtain data from SDSS
        query_galaxies = "select top 1 class, plate, mjd, fiberid, bestObjID from specObj where class = 'galaxy'"

        # Create a SpectralAnalysisBase Class instance to execute the queries
        galaxies = SpectralAnalysisBase(query_galaxies)
        galaxies.execute_query()  # Execute the query

        spectra_extractor = SpectraExtract(galaxies.data[0])
        spectra_data_valid = spectra_extractor.extract_spectra()
        
        return {
            'valid_data_row': galaxies.data[0],
            'invalid_data_row_incorrect_type': "invalid data row",
            'spectra_data_valid': spectra_data_valid,
            'spectra_data_incorrect_type': {'Wavelength': [9278.974, 7338.379, 7627.813, 8594.093, 5948.398, 4095.434, 9379.937, 4287.459],
                                    'Flux': [1.594, 43.589, 4.515, 40.433, 0.810, 8.621, 3.874, 8.888],
                                    'BestFit': [1.399, 44.233, 5.244, 40.825, 0.900, 9.443, 3.823, 8.430],
                                    'SkyFlux': [1.214, 4.007, 6.494, 2.608, 5.084, 3.056, 0.000, 2.698],
                                    }
        }

    @pytest.mark.usefixtures("setup_visualizer")
    def test_visualizer_with_both_row_and_data(self, setup_visualizer):
        """
        This is a trivial test to ensure that we raise a ValueError when both 
        DataFrame and Table.Row is passed
        """
        valid_data_row, invalid_data_row_incorrect_type, spectra_data_valid, spectra_data_incorrect_type = setup_visualizer.values()
        with pytest.raises(ValueError):
            visualizer = SpectralVisualizer(row=valid_data_row, data=spectra_data_valid)

    @pytest.mark.usefixtures("setup_visualizer")
    def test_visualizer_with_invalid_row_type(self, setup_visualizer):
        """
        This is a trivial test to ensure that we raise a TypeError when we do not
        pass in a row of type Table.Row
        """
        valid_data_row, invalid_data_row_incorrect_type, spectra_data_valid, spectra_data_incorrect_type = setup_visualizer.values()
        #match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."
        with pytest.raises(TypeError):
            visualizer = SpectralVisualizer(row=invalid_data_row_incorrect_type)

    @pytest.mark.usefixtures("setup_visualizer")
    def test_visualizer_with_invalid_data_type(self, setup_visualizer):
        """
        This is a trivial test to ensure that we raise a TypeError when we do not
        pass in spectral data of type DataFrame
        """
        valid_data_row, invalid_data_row_incorrect_type, spectra_data_valid, spectra_data_incorrect_type = setup_visualizer.values()
        # match="Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame."
        with pytest.raises(TypeError):
            visualizer = SpectralVisualizer(data=spectra_data_incorrect_type)

    @pytest.mark.usefixtures("setup_visualizer")
    def test_visualize_shows_graph_with_data(self, setup_visualizer):
        """
        This is a trivial test that ensures that something gets plotted when we 
        input valid data
        """
        valid_data_row, invalid_data_row_incorrect_type, spectra_data_valid, spectra_data_incorrect_type = setup_visualizer.values()

        matplotlib.use('Agg')
        
        visualizer = SpectralVisualizer(row=None, data=spectra_data_valid)

        #visualize data and confirm graph shows
        with patch('matplotlib.pyplot.show') as mock_show:
            visualizer.visualize()

        # Check if plt.show() was called
        mock_show.assert_called_once()

        # Reset the backend to the default
        plt.close('all')

    @pytest.mark.usefixtures("setup_visualizer")
    def test_visualize_shows_graph_with_row(self, setup_visualizer):
        """
        This is a trivial test that ensures that something gets plotted when we 
        input a valid table row
        """
        valid_data_row, invalid_data_row_incorrect_type, spectra_data_valid, spectra_data_incorrect_type = setup_visualizer.values()

        matplotlib.use('Agg')
        
        visualizer = SpectralVisualizer(row=valid_data_row, data=None)

         #visualize data and confirm graph shows
        with patch('matplotlib.pyplot.show') as mock_show:
            visualizer.visualize()

        # Check if plt.show() was called
        mock_show.assert_called_once()

        # Reset the backend to the default
        plt.close('all')
            

