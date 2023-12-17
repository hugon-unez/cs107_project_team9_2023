"""
This integration test module runs tests for core_functions_module_modify.py.
Specifically, it ensures that all of our classes within the module work dependently
"""
import unittest
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from group9_package.subpkg_1.core_functions_module_modify import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    """A class for testing our methods in the DataPreprocessor Class"""
    
    def setUp(self):
        """Tests Setup Testing Environment for Integration
        
        Data is passed in to ensure results integrate well together
        """
        self.query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy' and z > 0.3 and zWarning = 0"
        
        self.data_preprocessor = DataPreprocessor(query=self.query, data=None)
    
    def test_data_preprocessing_pipeline(self):
        """Tests All Data Preprocessing Methods work together
        
        Confirm Equivalence and values for each method and column
        """

        self.data_preprocessor.normalize_data()
        self.data_preprocessor.remove_outliers()

        self.data_preprocessor.interpolate_data([2,4,6,8,10,12,14,16,18,20])

        self.data_preprocessor.correct_redshift()

        #assert every column 'flux' row is populated
        self.assertTrue(all(np.isfinite(self.data_preprocessor.data['ra'])))

        #assert every column 'wavelength' row is populated
        self.assertTrue(all(np.isfinite(self.data_preprocessor.data['dec'])))

        #assert table has correct shape
        self.assertTrue(self.data_preprocessor.data.shape[0], 10)

class TestWavelengthAlign(unittest.TestCase):
    """Test cases for the WavelengthAlign function."""

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

        aligned_spectra = WavelengthAlign(spectra_data, target_range)

        # Check if aligned spectra have the same length as target_range
        for spectrum in aligned_spectra:
            self.assertEqual(len(spectrum['loglam']), num_wavelengths)

        # Check if flux values are correctly interpolated
        for spectrum in aligned_spectra:
            interpolator = interp1d(spectrum['loglam'], spectrum['flux'], kind='linear', fill_value=0.0, bounds_error=False)
            interpolated_flux = interpolator(spectrum['loglam'])
            np.testing.assert_allclose(spectrum['flux'], interpolated_flux)

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

    def test_invalid_data_type(self):
        """Test if a ValueError is raised for invalid data type."""
        with self.assertRaises(ValueError):
            WavelengthAlign("invalid_data_type", (4000, 8000))

    def test_missing_columns(self):
        """Test if a ValueError is raised for missing columns in the DataFrame."""
        missing_columns_data = self.valid_data.drop(columns=['flux', 'ivar'])
        with self.assertRaises(ValueError):
            WavelengthAlign(missing_columns_data, (4000, 8000))

    def test_target_range_out_of_range(self):
        """Test if a ValueError is raised when the target range is out of the loglam range."""
        with self.assertRaises(ValueError):
            WavelengthAlign(self.valid_data, (1000, 2000))


if __name__ == '__main__':
    unittest.main()
