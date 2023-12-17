"""This unit test module runs tests for core_functions_module_modify.py"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch
from astropy.table import Table
from scipy.interpolate import interp1d
from scipy.interpolate import interp1d
from group9_package.subpkg_1.core_functions_module_extract import SpectralAnalysisBase
from group9_package.subpkg_1.core_functions_module_modify import DataPreprocessor, WavelengthAlignment


class TestDataPreprocessor(unittest.TestCase):
    """A class for testing our methods in the DataPreprocessor Class"""
    def setUp(self):
        """
        Creating valid and invalid queries that we will use throughout the
        testing suite
        """
        self.valid_query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy' and z > 0.3 and zWarning = 0"
        self.invalid_query = "Invalid Query"

    def test_init_with_invalid_data(self):
        """Tests that we raise ValueError when invalid data is inputted"""
        with self.assertRaises(ValueError):
            DataPreprocessor(self.valid_query, data="invalid_data")

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_normalize_data(self, mock_query_sql):
        """Tests that we correctly normalize valid spectral data"""
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)
        data_preprocessor.normalize_data()

        for header in data_preprocessor.column_headers:
            normalized_data = (data[header] - np.mean(data[header])) / np.std(data[header])
            np.testing.assert_array_almost_equal(data_preprocessor.data[header], normalized_data)

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_remove_normalize_with_invalid_data(self, mock_query_sql):
        """Tests that we raise ValueError when trying normalize invalid spectral data"""
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        with self.assertRaises(ValueError):
            dataPre = DataPreprocessor(self.valid_query, data=data)
            dataPre.data = None
            dataPre.normalize_data()

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_remove_outliers(self, mock_query_sql):
        """Tests that we correctly remove outliers from valid spectral data"""
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)
        data_preprocessor.remove_outliers()

        for header in data_preprocessor.column_headers:
            z_scores = np.abs((data[header] - np.mean(data[header])) / np.std(data[header]))
            outliers_removed = data[header][z_scores < 2.5]
            np.testing.assert_array_almost_equal(data_preprocessor.data[header], outliers_removed)

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_remove_outliers_with_invalid_data(self, mock_query_sql):
        """Tests that we raise ValueError when trying remove outliers from invalid spectral data"""
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        with self.assertRaises(ValueError):
            dataPre = DataPreprocessor(self.valid_query, data=data)
            dataPre.data = None
            dataPre.remove_outliers()

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_interpolate_data(self, mock_query_sql):
        """Tests that we correctly interpolate valid spectral data"""
        data = pd.DataFrame({'ra': [1, 2, 3,7], 'u': [7, 8, 9, 15]})
        mock_query_sql.return_value = Table.from_pandas(data)
        test_data = data.copy()
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)

        new_wavelengths = np.array([1.2, 1.5, 2.9, 4])
        data_preprocessor.interpolate_data(new_wavelengths)

        interp_function = interp1d(test_data['ra'], test_data['u'], kind='cubic', fill_value="extrapolate", bounds_error=False)
        interpolated_values = interp_function(new_wavelengths)
        np.testing.assert_array_almost_equal(data_preprocessor.data['u'], interpolated_values)

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_interpolation_with_invalid_data(self, mock_query_sql):
        """Tests that we raise ValueError when trying interpolate invalid spectral data"""
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        with self.assertRaises(ValueError):
            dataPre = DataPreprocessor(self.valid_query, data=data)
            dataPre.data = None
            new_wavelengths = np.array([1, 1.2, 1.3])
            dataPre.interpolate_data(new_wavelengths)
    
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_correct_redshift(self, mock_query_sql):
        """Tests that we correctly correct redshift in valid spectral data"""
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        test_data = data.copy()
        mock_query_sql.return_value = Table.from_pandas(data)
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)
        bands = ['u', 'g', 'r', 'i']
        data_preprocessor.correct_redshift(bands)

        for band in bands:
            corrected_values = test_data[band] / (1 + test_data['z'])
            np.testing.assert_array_almost_equal(data_preprocessor.data[band], corrected_values)

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_redshift_with_invalid_data(self, mock_query_sql):
        """Tests that we raise ValueError when trying correct redshift in invalid spectral data"""
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        with self.assertRaises(ValueError):
            dataPre = DataPreprocessor(self.valid_query, data=data)
            dataPre.data = None
            dataPre.correct_redshift()

class TestWavelengthAlignment(unittest.TestCase):
    """Test cases for the WavelengthAlignment Class."""

    def setUp(self):
        """Set up valid data for testing."""
        # Sample valid spectra data
        self.valid_data = pd.DataFrame({
            'loglam': np.linspace(4000, 8000, 100),
            'flux': np.random.rand(100),
            'ivar': np.random.rand(100),
            'and_mask': np.zeros(100, dtype=int),
            'or_mask': np.zeros(100, dtype=int),
            'wdisp': np.random.rand(100),
            'sky': np.random.rand(100),
            'model': np.random.rand(100)
        })

    def test_alignment(self):
        """Test the alignment of spectra data."""
        # Create sample spectra data
        num_spectra = 5
        num_wavelengths = 100
        target_range = (5000, 7000)
        spectra_data = []

        for _ in range(num_spectra):
            loglam = np.linspace(target_range[0], target_range[1], num_wavelengths)
            flux = np.random.rand(num_wavelengths) * 100  # Random flux values
            ivar = np.random.rand(num_wavelengths) * 10    # Random inverse variance
            and_mask = np.zeros(num_wavelengths, dtype=int)
            or_mask = np.zeros(num_wavelengths, dtype=int)
            wdisp = np.random.rand(num_wavelengths) * 2    # Random wdisp values
            sky = np.random.rand(num_wavelengths) * 50     # Random sky values
            model = np.random.rand(num_wavelengths) * 200  # Random model values

            spectra_data.append({
                'loglam': loglam,
                'flux': flux,
                'ivar': ivar,
                'and_mask': and_mask,
                'or_mask': or_mask,
                'wdisp': wdisp,
                'sky': sky,
                'model': model
            })

        aligned_spectra = WavelengthAlignment.WavelengthAlign(pd.DataFrame(spectra_data), target_range)

        # Check if aligned spectra have the same length as target_range
        for spectrum in aligned_spectra:
            self.assertEqual(len(spectrum['loglam']), num_wavelengths)

        # Check if flux values are correctly interpolated
        for spectrum in aligned_spectra:
            interpolator = interp1d(spectrum['loglam'], spectrum['flux'], kind='linear', fill_value=0.0, bounds_error=False)
            interpolated_flux = interpolator(spectrum['loglam'])
            np.testing.assert_allclose(spectrum['flux'], interpolated_flux)

    def test_invalid_data_type(self):
        """Test if a ValueError is raised for invalid data type."""
        with self.assertRaises(ValueError):
            WavelengthAlignment.WavelengthAlign("invalid_data_type", (4000, 8000))

    def test_missing_columns(self):
        """Test if a ValueError is raised for missing columns in the DataFrame."""
        missing_columns_data = self.valid_data.drop(columns=['flux', 'ivar'])
        with self.assertRaises(ValueError):
            WavelengthAlignment.WavelengthAlign(missing_columns_data, (4000, 8000))

    def test_target_range_out_of_range(self):
        """Test if a ValueError is raised when the target range is out of the loglam range."""
        with self.assertRaises(ValueError):
            WavelengthAlignment.WavelengthAlign(self.valid_data, (1000, 2000))

if __name__ == '__main__':
    unittest.main()