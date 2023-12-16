#!/usr/bin/env python3
# File       : machine_learning_module.py
# Description: Classify Galaxy, Star, or QSO based on spectral data
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.
"""This python module provides functionality to predict a celestial object based on its spectral data"""

from astropy.table import Table
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd

class CelestialObjectClassifier:
    """A class for classifying a Star, Galaxy, or QSO"""
    def __init__(self, X_train = None, X_test = None, model_fit = False):
        """Initializes the CelestialObjectClassifier Class

        Args:
            X_train: Data used to train the logisitic regression model
                Defaults to None.
            X_test: Data used to predict the type of celestial object
                Defaults to None.
            model_fit: Boolean that indicates whether or not the model has been
                trained. Defaults to False.
        """
        self.X_train = X_train
        self.X_test = X_test
        self.model_fit = model_fit
        self.model = LogisticRegression()  # Using Logistic Regression as an example

    def fit(self, spectral_data, y):
        """Trains model based on given spectral data and classifications
        
        Args:
            spectral_data (DataFrame): Data used to train the logisitic regression model
            y (Series): Classes (QSO, Star, or Galaxy) for each observation in our data
        """
        if (not isinstance(spectral_data, pd.DataFrame) or not isinstance(y, pd.Series)):
            raise ValueError("Spectral Data inputted not a data frame or classifications data not a series")

        if (spectral_data.empty or y.empty):
            raise ValueError("Not enough data inputted to train model")

        self.X_train = spectral_data

        self.model_fit = True

        # Train the model
        self.model.fit(self.X_train, y)

    def predict(self, spectral_data, y):
        """Predicts the class for each observation in the dataset 
        
        Args:
            spectral_data (DataFrame): Data used to predict the class of celestial object
            y (Series): Classes (QSO, Star, or Galaxy) for each observation in our data, so that we can generate 
                the confusion matrix

        Returns:
            Series, where each element represents the predicted class for an observation

        Outputs:
            Confusion Matrix, where all elemenets in the first row sum to get the 
            true number of galaxies, and the first element of the row represents
            the number of correctly predicted galaxies from our model; where all
            elements in the second row sum to get the true number of stars, and 
            the second element of the row represents the number of correctly 
            predicted stars from our model; where all elements in the third row
            sum to get the true number of qsos, and the third element of the row
            represents the number of correctly predicted qsos from our model
        """
        if (not isinstance(spectral_data, pd.DataFrame) or not isinstance(y, pd.Series)):
            raise ValueError("Spectral Data inputted not a data frame or classifications data not a series")

        if not self.model_fit:
            raise ValueError("Need to train model first")

        if (spectral_data.empty or y.empty):
            raise ValueError("Not enough data inputted to predict")

        self.X_test = spectral_data

        # Ensure predicting data has the same format as training data
        if self.X_train.shape[1] != self.X_test.shape[1]:
            raise ValueError("Number of features in the test data not the same as train data")

        # Make predictions on the test set
        y_pred = self.model.predict(self.X_test)

        # Generate and display confusion matrix
        conf_matrix = confusion_matrix(y, y_pred, labels=["galaxy", "star", "qso"])
        print("Confusion Matrix:")
        print(conf_matrix)

        return y_pred

    def predict_proba(self, spectral_data):
        """Predicts the probabilities that an observation is a Galaxy, Stary, or QSO
 
        Args:
            spectral_data: Data used to predict the class of celestial object

        Returns: 
            dataframe, where each row represents an observation and the columns represent 
            the probability that this observation is either a Stars, Galaxy, or QSO
        """
        if not isinstance(spectral_data, pd.DataFrame):
            raise ValueError("Data inputted not a dataframe")

        if not self.model_fit:
            raise ValueError("Need to train model first")

        if spectral_data.empty:
            raise ValueError("Not enough data inputted to predict")

        self.X_test = spectral_data

        # Ensure predicting data has the same format as training data
        if self.X_train.shape[1] != self.X_test.shape[1]:
            raise ValueError("Number of features in the test data not the same as train data")

        return self.model.predict_proba(self.X_test)
