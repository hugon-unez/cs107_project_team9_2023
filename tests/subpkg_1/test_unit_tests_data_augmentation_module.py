from astroquery.sdss import SDSS
import pytest
import unittest
import numpy as np
import pandas as pd
import differint.differint as df
from group9_package.subpkg_1.data_augmentation_module import DataAugmentation

class TestDataPreprocessor(unittest.TestCase):
    """A class for testing our methods in the Data Augmentation Module"""
    def setUp(self):
        """
        Creating valid and invalid spectra data that we will use throughout the
        testing suite
        """
        self.valid_data = pd.DataFrame({'Wavelength': [9278.974, 7338.379, 7627.813, 8594.093, 5948.398, 4095.434, 9379.937, 4287.459],
                                            'Flux': [1.594, 43.589, 4.515, 40.433, 0.810, 8.621, 3.874, 8.888],
                                            'BestFit': [1.399, 44.233, 5.244, 40.825, 0.900, 9.443, 3.823, 8.430],
                                            'SkyFlux': [1.214, 4.007, 6.494, 2.608, 5.084, 3.056, 0.000, 2.698],
                                            })
        self.invalid_data = "Invalid Data"
    
    def test_init_with_invalid_data_type(self):
        """
        This is a trivial test to ensure that we raise a TypeError when we do not
        pass in a data of type pd.DataFrame
        """
        
        with pytest.raises(TypeError):
            data_augmentor = DataAugmentation(data=self.invalid_data)

    def test_derivative_with_invalid_column_name(self):
        """
        This is a trivial test to ensure that we raise a ValueError when we do not
        pass in a valid column name within the data for derivative function
        """
        
        with pytest.raises(ValueError):
            data_augmentor = DataAugmentation(data=self.valid_data)
            data_augmentor.compute_derivative(column_name="Invalid Column")

    def test_fractional_derivative_with_invalid_column_name(self):
        """
        This is a trivial test to ensure that we raise a ValueError when we do not
        pass in a valid column name within the data for fractional derivative function
        """
        
        with pytest.raises(ValueError):
            data_augmentor = DataAugmentation(data=self.valid_data)
            data_augmentor.compute_fractional_derivative(column_name="Invalid Column", derivative_order=0.5)

    def test_derivative_with_valid_data(self):
        """
        This test confirms that the derivative function correctly outputs 
        correctly outputs an additional column in name
        """
        
        data_augmentor = DataAugmentation(data=self.valid_data)
        data_augmentor.compute_derivative(column_name="Flux")

        # make sure dataframe has correct columns
        self.assertCountEqual(['Wavelength', 'Flux', 'BestFit', 'SkyFlux','Flux Derivative'], data_augmentor.data)

    def test_fractional_derivative_with_valid_data(self):
        """
        This test confirms that the fractional derivative function correctly
        outputs an additional column in data
        """
        
        data_augmentor = DataAugmentation(data=self.valid_data)
        data_augmentor.compute_fractional_derivative(column_name="Flux", derivative_order=0.5)

        # make sure dataframe has correct columns
        self.assertCountEqual(['Wavelength', 'Flux', 'BestFit', 'SkyFlux', 'Flux_fractional_derivative'], data_augmentor.data)

    def test_augment_derivatives_with_valid_data(self):
        """
        This test confirms that both derivative functions correctly
        output an additional columns in data
        """
        
        data_augmentor = DataAugmentation(data=self.valid_data)
        data_augmentor.augment_both_derivatives(column_name="Flux", derivative_order=0.5)

        # make sure dataframe has correct columns
        self.assertCountEqual(['Wavelength', 'Flux', 'BestFit', 'SkyFlux','Flux Derivative','Flux_fractional_derivative'], data_augmentor.data)

    def test_augment_derivatives_with_valid_data(self):
        """
        This test confirms two of the row values for the derivatives calculated
        """
        
        data_augmentor = DataAugmentation(data=self.valid_data)
        data_augmentor.augment_both_derivatives(column_name="Flux", derivative_order=0.5)

        # make sure last row data matches for derivative column
        np.testing.assert_almost_equal(data_augmentor.data['Flux Derivative'][7], 5.014, decimal=2)

        # make sure last row data matches for fractional derivative column
        np.testing.assert_almost_equal(data_augmentor.data['Flux_fractional_derivative'][7], 7.22, decimal=2)