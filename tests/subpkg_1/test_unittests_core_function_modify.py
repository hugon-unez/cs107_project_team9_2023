import unittest
from unittest.mock import patch
from astropy.table import Table
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from group9_package.subpkg_1.core_functions_module_extract import SpectralAnalysisBase
from group9_package.subpkg_1.core_functions_module_modify import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        self.valid_query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy' and z > 0.3 and zWarning = 0"
        self.invalid_query = "Invalid Query"

    # Test initialization with invalid data
    def test_init_with_invalid_data(self):
        with self.assertRaises(ValueError):
            DataPreprocessor(self.valid_query, data="invalid_data")

    # Test normalization
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_normalize_data(self, mock_query_sql):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)
        data_preprocessor.normalize_data()

        for header in data_preprocessor.column_headers:
            normalized_data = (data[header] - np.mean(data[header])) / np.std(data[header])
            print(normalized_data)
            print("zach")
            print(data_preprocessor.data[header])
            np.testing.assert_array_almost_equal(data_preprocessor.data[header], normalized_data)

    # Test remove normalize with invalid data
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_remove_normalize_with_invalid_data(self, mock_query_sql):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        with self.assertRaises(ValueError):
            dataPre = DataPreprocessor(self.valid_query, data=data)
            dataPre.data = None
            dataPre.normalize_data()

    # Test outlier removal
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_remove_outliers(self, mock_query_sql):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)
        data_preprocessor.remove_outliers()

        for header in data_preprocessor.column_headers:
            z_scores = np.abs((data[header] - np.mean(data[header])) / np.std(data[header]))
            outliers_removed = data[header][z_scores < 2.5]
            np.testing.assert_array_almost_equal(data_preprocessor.data[header], outliers_removed)

    # Test remove outliers with invalid data
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_remove_outliers_with_invalid_data(self, mock_query_sql):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        with self.assertRaises(ValueError):
            dataPre = DataPreprocessor(self.valid_query, data=data)
            dataPre.data = None
            dataPre.remove_outliers()

    # Test interpolation
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_interpolate_data(self, mock_query_sql):
        data = pd.DataFrame({'ra': [1, 2, 3,7], 'u': [7, 8, 9,15]})
        mock_query_sql.return_value = Table.from_pandas(data)
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)

        new_wavelengths = np.array([1.2, 1.5, 2.9, 4])
        data_preprocessor.interpolate_data(new_wavelengths)

        interp_function = interp1d(data['ra'], data['u'], kind='cubic', fill_value="extrapolate", bounds_error=False)
        interpolated_values = interp_function(new_wavelengths)
        np.testing.assert_array_almost_equal(data_preprocessor.data['u'], interpolated_values)

    # Test interpolation with invalid data
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_interpolation_with_invalid_data(self, mock_query_sql):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        with self.assertRaises(ValueError):
            dataPre = DataPreprocessor(self.valid_query, data=data)
            dataPre.data = None
            new_wavelengths = np.array([1, 1.2, 1.3])
            dataPre.interpolate_data(new_wavelengths)
    
    # Test redshift correction
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_correct_redshift(self, mock_query_sql):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)

        bands = ['u', 'g', 'r', 'i']
        data_preprocessor.correct_redshift(bands)

        for band in bands:
            corrected_values = data[band] / (1 + data['z'])
            np.testing.assert_array_almost_equal(data_preprocessor.data[band], corrected_values)

    # Test redshifts with invalid data
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_redshift_with_invalid_data(self, mock_query_sql):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = Table.from_pandas(data)
        with self.assertRaises(ValueError):
            dataPre = DataPreprocessor(self.valid_query, data=data)
            dataPre.data = None
            dataPre.correct_redshift()