"""
This integration test module runs tests for machine_learning_module.py.
Specifically, it ensures that the module works with the core_functions_module_extract
"""
import pytest
from astropy.table import Table
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from group9_package.subpkg_2.machine_learning_module import CelestialObjectClassifier
from group9_package.subpkg_1.core_functions_module_extract import SpectralAnalysisBase, MetaDataExtractor, SpectraExtract


class TestCelestialObjectClassifier():
    """A class for testing our methods in machine_learning_module"""
    @pytest.fixture
    def setup_celestial_classifier(self):
        """Define pytest fixtures for X_train, X_test, y_train, y_test"""
        # Define a sample ADQL queries to obtain data from SDSS
        query_galaxies = "select top 1 class, plate, mjd, fiberid, bestObjID from specObj where class = 'galaxy'"
        query_stars = "select top 1 class, plate, mjd, fiberid, bestObjID from specObj where class = 'star'"
        query_qsos = "select top 1 class, plate, mjd, fiberid, bestObjID from specObj where class = 'qso'"

        # Create a SpectralAnalysisBase Class instances to execute the queries
        galaxies = SpectralAnalysisBase(query_galaxies)
        galaxies.execute_query()  # Execute the query


        stars = SpectralAnalysisBase(query_stars)
        stars.execute_query()  # Execute the query

        qsos = SpectralAnalysisBase(query_qsos)
        qsos.execute_query() # Execute the query

        # Create empty lists to store spectral data and classifications
        spectral_data = []
        classifications = []

        # Function to extract spectral data and classifications
        def process_data(query_data, classification):
            for row in query_data:
                spectra_extractor = SpectraExtract(row)
                spectra_data = spectra_extractor.extract_spectra()
                spectral_data.append(spectra_data)
                for _ in range(len(spectra_data)):
                    classifications.append([classification])

        # Process galaxies data
        process_data(galaxies.data, "galaxy")

        # Process stars data
        process_data(stars.data, "star")

        # Process qsos data
        process_data(qsos.data, "qso")

        # Create a DataFrame for spectral data
        spectral_df = pd.concat(spectral_data, ignore_index=True)

        # Create a DataFrame 'y' for classifications
        y = pd.DataFrame(classifications, columns=["Classification"])

        # Horizontally stack spectral_df and classifications
        stacked_df = pd.concat([spectral_df, y], axis=1)

        train_data, test_data = train_test_split(stacked_df, test_size=0.2, random_state=42)

        X_train, y_train = train_data.drop(columns=["Classification"]), train_data["Classification"] 

        X_test, y_test = test_data.drop(columns=["Classification"]), test_data["Classification"] 
        
        return {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        }

    @pytest.mark.usefixtures("setup_celestial_classifier")
    def test_init(self, setup_celestial_classifier):
        """This is a trivial test that our class has the appropriate instance variables"""

        X_train, X_test, y_train, y_test = setup_celestial_classifier.values()

        # Initializing Classifier  Class
        classifier = CelestialObjectClassifier()

        assert hasattr(classifier, "X_train")
        assert hasattr(classifier, "X_test")
        assert hasattr(classifier, "model_fit")
        assert hasattr(classifier, "model")

    @pytest.mark.usefixtures("setup_celestial_classifier")
    def test_fit(self, setup_celestial_classifier):
        """This is a trivial test that tests the fit function

        Specifically, it ensures that we set the instance variable X_train
        and do not try and fit the model on empty data
        """

        X_train, X_test, y_train, y_test = setup_celestial_classifier.values()

        classifier = CelestialObjectClassifier()

        with pytest.raises(ValueError):
            classifier.fit(pd.DataFrame(), y_train)

        with pytest.raises(ValueError):
            classifier.fit(X_train, pd.DataFrame())

        with pytest.raises(ValueError):
            classifier.predict("pd.DataFrame()", y_train)

        classifier.fit(X_train, y_train)

        assert (classifier.model_fit == True)

    @pytest.mark.usefixtures("setup_celestial_classifier")
    def test_predict(self, setup_celestial_classifier):
        """This is a trivial test that tests the predict function

        Specifically, it ensures that we set the instance variable X_test,
        do not try and predict on empty data, do not try to predict if 
        the model is not trained, or do not try to predict on data that does not 
        have the right amount of columns. Additionally, it ensures that our 
        predictions is a n x 1 series
        """

        X_train, X_test, y_train, y_test = setup_celestial_classifier.values()

        classifier = CelestialObjectClassifier()

        with pytest.raises(ValueError):
            classifier.predict(pd.DataFrame(), y_train)

        with pytest.raises(ValueError):
            classifier.predict(X_train, pd.DataFrame())

        with pytest.raises(ValueError):
            classifier.predict(X_train, y_train)

        with pytest.raises(ValueError):
            classifier.predict("pd.DataFrame()", y_train)

        classifier.fit(X_train, y_train)

        # Get the label of the last column
        last_column_label = X_test.columns[-1]

        # Drop the last column
        dropped_column_X_test = X_test.drop(columns=last_column_label, inplace=False)

        with pytest.raises(ValueError):
            classifier.predict(dropped_column_X_test, y_test)

        predictions = classifier.predict(X_test, y_test)

        assert (predictions.shape[0] == y_test.shape[0])

    @pytest.mark.usefixtures("setup_celestial_classifier")
    def test_predict_proba(self, setup_celestial_classifier):
        """This is a trivial test that tests the predict_proba function

        Specifically, it ensures that we set the instance variable X_test,
        do not try and run predict_proba on empty data, do not try to predict
        if the model is not trained, or do not try to predict on data that does not 
        have the right amount of columns. It also ensures that the predictions 
        we get back is a n x 3 matrix
        """

        X_train, X_test, y_train, y_test = setup_celestial_classifier.values()

        classifier = CelestialObjectClassifier()

        with pytest.raises(ValueError):
            classifier.predict_proba(pd.DataFrame())

        with pytest.raises(ValueError):
            classifier.predict_proba(X_train)

        with pytest.raises(ValueError):
            classifier.predict_proba("pd.DataFrame()")

        classifier.fit(X_train, y_train)

        # Get the label of the last column
        last_column_label = X_test.columns[-1]

        # Drop the last column
        dropped_column_X_test = X_test.drop(columns=last_column_label, inplace=False)

        with pytest.raises(ValueError):
            classifier.predict_proba(dropped_column_X_test)

        prediction_probabilities = classifier.predict_proba(X_test)

        assert (prediction_probabilities.shape == (y_test.shape[0],3))
