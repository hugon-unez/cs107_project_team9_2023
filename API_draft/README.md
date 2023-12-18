# CS107 Final Project - Team 9
[![.github/workflows/coverage.yml](https://code.harvard.edu/CS107/team09_2023/actions/workflows/coverage.yml/badge.svg)](https://code.harvard.edu/CS107/team09_2023/actions/workflows/coverage.yml)

[![.github/workflows/tests.yml](https://code.harvard.edu/CS107/team09_2023/actions/workflows/tests.yml/badge.svg)](https://code.harvard.edu/CS107/team09_2023/actions/workflows/tests.yml)

# Core Functions Module Extract

## Class: Base
Executes Query (if given) and stores data (from executed query or from passed argument) as an attribute.

### Functions:
- `__init__`: Initializes appropriate attributes.
- `execute_query`: Executes the query (if given) and stores the data.

## Class: MetadataExtractor
Inherits Base Class.
Extracts metadata, including class, from the spectral data.

### Functions:
- `__init__`: Initializes appropriate attributes.
- `extract_identifiers(data)`: Extracts identifiers from the data either passed to the class or data from an executed query.
- `extract_coordinates`: Extracts coordinates from the data either passed to the class or data from an executed query.
- `extract_chemical_abundances`: Extracts chemical abundances from the data either passed to the class or data from an executed query.
- `extract_redshifts`: Extracts redshift values from the data either passed to the class or data from an executed query associated with each celestial object.

# Core Functions Module Modify

## Class: WavelengthAlign
Inherits Base Class.
Aligns wavelength for all the spectra across a predefined range.
Returns a flux value.

### Functions:
- `__init__`: Initializes appropriate attributes.
- `align_wavelengths`: The main function responsible for aligning the wavelengths. This could involve interpolation or resampling to ensure that all spectra share the same set of wavelengths within the predefined range.

## Class: DataPreprocessor
Inherits Base Class.
Manages data preprocessing tasks for each spectrum independently.

### Functions:
- `__init__`: Initializes appropriate attributes.
- `normalize_data`: Normalizes the data either passed to the class or data from an executed query.
- `remove_outliers`: Removes outliers from the data either passed to the class or data from an executed query.
- `interpolate_data`: Performs interpolation on the data either passed to the class or data from an executed query.
- `correct_redshift`: Adjusts the wavelengths of the spectral data based on the redshift values associated with each celestial object.

# Visualization Module

## Class: Visualize
Visualizes metadata after extraction/alignment.

### Imports:
- Core Functions Module

### Functions:
- `visualize`: Entire function uses matplotlib to handle all visualization queries in a single call.

# Data Augmentation Module

## Class: Augment
Computes derivatives/fractional derivatives and appends them to each preprocessed spectra.

### Functions:
- `__init__`: Initializes appropriate attributes.
- `compute_derivative`: Computes the derivative for each spectrum in the input data.
- `compute_fractional_derivative`: Computes the fractional derivative for each spectrum based on the specified order.
- `append_derivatives`: Appends the computed derivatives to each spectrum in the input data.
- `append_fractional_derivatives`: Appends the computed fractional derivatives to each spectrum in the input data.
- `augment_data`: Combines all the above steps to perform the complete data augmentation process.

# Cross-Matching Module

## Class: CrossMatch
Cross matches data with other reference sources.

### Functions:
- `__init__`: Takes in query and the data source to cross-reference.
- `cross_match(data1, data2)`: Takes in two tables and calculates the match purity.

# Machine Learning Module

## Class: Classification
Distinguishes between Stars, Galaxies, and QSOs using spectral data. 

### Functions:
- `__init__`: Initializes appropriate attributes.
- `get_params`: Retrieves the params dictionary.
- `set_params`: Sets the intercept and coefficient keys within the params dictionary.
- `fit`: Sets the model's parameters based on the provided data.
- `predict`: Predicts the class for each observation in the dataset provided (X).
- `predict_proba`: Returns a dataframe where each row represents an observation, and each column represents the probability of being a part of Stars, Galaxies, and QSOs.

