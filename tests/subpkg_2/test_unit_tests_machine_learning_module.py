"""This unit test module runs tests for machine_learning_module.py"""

import unittest
import sys
import pandas as pd
import numpy as np
from io import StringIO
from pandas.testing import assert_frame_equal
from group9_package.subpkg_2.machine_learning_module import CelestialObjectClassifier

class TestCelestialObjectClassifier(unittest.TestCase):
    """A class for testing our methods in the CelestialObjectClassifier Class"""
    def setUp(self):
        """Create Train and Test spectral data"""
        self.spectral_data_train = pd.DataFrame({'Wavelength': [9278.974, 7338.379, 7627.813, 8594.093, 5948.398, 4095.434, 9379.937, 4287.459],
                                            'Flux': [1.594, 43.589, 4.515, 40.433, 0.810, 8.621, 3.874, 8.888],
                                            'BestFit': [1.399, 44.233, 5.244, 40.825, 0.900, 9.443, 3.823, 8.430],
                                            'SkyFlux': [1.214, 4.007, 6.494, 2.608, 5.084, 3.056, 0.000, 2.698],
                                            })
        self.y_train = pd.Series(["galaxy", "star", "qso", "star", "galaxy", "star", "qso", "star"])

        self.spectral_data_test = pd.DataFrame({'Wavelength': [4395.415, 6609.977],
                                           'Flux': [0.487, 43.941], 
                                           'BestFit': [0.237, 42.118],
                                           'SkyFlux': [2.552, 2.631],
                                           })
        self.y_test = pd.Series(["galaxy", "star"])

    def test_fit_incorrect_types(self):
        """
        Tests that we raise ValueError when data of incorrect type is inputted into
        the fit method
        """
        classifier = CelestialObjectClassifier()
        with self.assertRaises(ValueError):
            classifier.fit(spectral_data=self.spectral_data_train, y=[["galaxy"], ["star"]])

        with self.assertRaises(ValueError):
            classifier.fit(spectral_data={'Wavelength': [9278.974, 7338.379, 7627.813, 8594.093, 5948.398, 4095.434, 9379.937, 4287.459],
                                            'Flux': [1.594, 43.589, 4.515, 40.433, 0.810, 8.621, 3.874, 8.888],
                                            'BestFit': [1.399, 44.233, 5.244, 40.825, 0.900, 9.443, 3.823, 8.430],
                                            'SkyFlux': [1.214, 4.007, 6.494, 2.608, 5.084, 3.056, 0.000, 2.698],
                                        }, 
                            y=self.y_train)
                        
    def test_fit_empty_data(self):
        """
        Tests that we raise ValueError when empty data is inputted into
        the fit method
        """
        classifier = CelestialObjectClassifier()
        with self.assertRaises(ValueError):
            classifier.fit(spectral_data=pd.DataFrame(), y=self.y_train)

        with self.assertRaises(ValueError):
            classifier.fit(spectral_data=self.spectral_data_train, y=pd.Series())

    def test_fit_valid(self):
        """
        Tests that X_train instance variable is set and model_fit is set if 
        valid data is inputted into the fit method
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        assert_frame_equal(classifier.X_train, self.spectral_data_train)

        self.assertEqual(classifier.model_fit, True)

    def test_predict_no_train(self):
        """
        Tests that we raise ValueError when trying to predict before training
        """
        classifier = CelestialObjectClassifier()
        with self.assertRaises(ValueError):
            classifier.predict(spectral_data=self.spectral_data_test, y=self.y_test)

    def test_predict_incorrect_types(self):
        """
        Tests that we raise ValueError when data of incorrect type is inputted into
        the predict method
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        with self.assertRaises(ValueError):
            classifier.predict(spectral_data=self.spectral_data_test, y=[["galaxy"], ["star"]])

        with self.assertRaises(ValueError):
            classifier.predict(spectral_data={'Wavelength': [9278.974, 7338.379, 7627.813, 8594.093, 5948.398, 4095.434, 9379.937, 4287.459],
                                            'Flux': [1.594, 43.589, 4.515, 40.433, 0.810, 8.621, 3.874, 8.888],
                                            'BestFit': [1.399, 44.233, 5.244, 40.825, 0.900, 9.443, 3.823, 8.430],
                                            'SkyFlux': [1.214, 4.007, 6.494, 2.608, 5.084, 3.056, 0.000, 2.698],
                                        }, 
                            y=self.y_test)

    def test_predict_empty_data(self):
        """
        Tests that we raise ValueError when empty data is inputted into
        the predict method
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        with self.assertRaises(ValueError):
            classifier.predict(spectral_data=pd.DataFrame(), y=self.y_test)

        with self.assertRaises(ValueError):
            classifier.predict(spectral_data=self.spectral_data_test, y=pd.Series())

    def test_predict_mismatching_test_train(self):
        """
        Tests that we raise ValueError when test data does not have same number of
        columns as train data
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        # Get the label of the last column
        last_column_label = self.spectral_data_test.columns[-1]

        # Drop the last column
        dropped_column_test = self.spectral_data_test.drop(columns=last_column_label, inplace=False)

        with self.assertRaises(ValueError):
            classifier.predict(spectral_data=dropped_column_test, y=self.y_test)

    def test_predict_valid_data(self):
        """
        Tests that returned predictions is of correct shape and that something gets
        printed to stdout
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        # Capture the standard output
        captured_output = StringIO()
        sys.stdout = captured_output

        predictions = classifier.predict(spectral_data=self.spectral_data_test, y=self.y_test)

        # Reset the standard output
        sys.stdout = sys.__stdout__

        # Check if something has been printed (i.e., the output is not empty)
        self.assertTrue(captured_output.getvalue())  # This will check if the captured output is not an empty string

        self.assertEqual(predictions.shape[0], self.y_test.shape[0])

    def test_predict_pronba_no_train(self):
        """
        Tests that we raise ValueError when trying to predict probabilities before training
        """
        classifier = CelestialObjectClassifier()
        with self.assertRaises(ValueError):
            classifier.predict_proba(spectral_data=self.spectral_data_test)

    def test_predict_proba_incorrect_types(self):
        """
        Tests that we raise ValueError when data of incorrect type is inputted into
        the predict_proba method
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        with self.assertRaises(ValueError):
            classifier.predict_proba(spectral_data={'Wavelength': [9278.974, 7338.379, 7627.813, 8594.093, 5948.398, 4095.434, 9379.937, 4287.459],
                                            'Flux': [1.594, 43.589, 4.515, 40.433, 0.810, 8.621, 3.874, 8.888],
                                            'BestFit': [1.399, 44.233, 5.244, 40.825, 0.900, 9.443, 3.823, 8.430],
                                            'SkyFlux': [1.214, 4.007, 6.494, 2.608, 5.084, 3.056, 0.000, 2.698],
                                        })

    def test_predict_proba_empty_data(self):
        """
        Tests that we raise ValueError when empty data is inputted into
        the predict_proba method
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        with self.assertRaises(ValueError):
            classifier.predict_proba(spectral_data=pd.DataFrame())

    def test_predict_proba_mismatching_test_train(self):
        """
        Tests that we raise ValueError when test data does not have same number of
        columns as train data
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        # Get the label of the last column
        last_column_label = self.spectral_data_test.columns[-1]

        # Drop the last column
        dropped_column_test = self.spectral_data_test.drop(columns=last_column_label, inplace=False)

        with self.assertRaises(ValueError):
            classifier.predict_proba(spectral_data=dropped_column_test)

    def test_predict_proba_valid_data(self):
        """
        Tests that returned prediction probabilities is of correct shape
        """
        classifier = CelestialObjectClassifier()
        classifier.fit(spectral_data=self.spectral_data_train, y=self.y_train)

        prediction_probabilities = classifier.predict_proba(spectral_data=self.spectral_data_test)
       
        self.assertEqual(prediction_probabilities.shape, (self.y_test.shape[0],3))

if __name__ == '__main__':
    unittest.main()