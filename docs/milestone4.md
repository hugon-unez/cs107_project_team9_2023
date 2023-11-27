# Structure of Directory

- LICENSE
	- Rationale: We chose to use this license because we feel that any modifications to the library itself must be free and usable by everyone. This license follows the copyleft standard; however, we believe that proprietary software can use our library if they do not make any changes or modifications to the library. We believe a company does not have to release their proprietary software if they do not modify our library and are free to advertise their software. In regards to patents, we do not have to worry about them because the library will be free to use by everyone and all modifications will be free to use. We believe that it makes the most sense to allow modifications to the library in the case that next year's CS107 project potentially can modify this library. Furthermore, we chose to use a copyleft license to make sure that we were in accordance and compatible with any of the licenses for the libraries we import in our modules.

- README

- src
	- group9_package
		- __init__.py

		- subpkg_1
			- __init__.py
			- core_functions_module.py
			- visualization_module.py
			- data_augmentation_module.py

		- subpkg_2
			- __init__.py
			- machine_learning_module.py
			- cross_matching_module.py

	- tests
		- __init__.py

		- subpkg_1
			- test_core_functions_module.py
				- Class TestBase
					- def test_execute_query
				- Class TestDataPreprocessor
					- def test_normalize_data
					- def test_remove_outliers
					- def test_interpolate_data
					- def test_correct_redshift
				- Class TestMetadataExtractor
					- def test_extract_identifiers
					- def test_extract_coordinates	
					- def test_extract_chemical_abundances
					- def test_extract_redshifts
				- Class TestWavelengthAlign
					- def test_align_wavelengths
			-  test_visualization_module.py
				- Class TestVisualize
					- def test_visualize_function
			- test_data_augmentation_module.py
				- Class TestAugment
					- def test_compute_derivative
					- def test_compute_fractional_derivative
					- def test_append_derivatives
					- def test_append_fractional_derivatives
					- def test_augment_data

		- subpkg_2
			- test_machine_learning_module.py
				- Class TestClassification
					- def test_get_params
					- def test_set_params
					- def test_fit
					- def test_predict
					- def test_predict_proba
			- test_Cross_matching_module.py
				- Class TestCrossMatch
					- def test_cross_match

- docs
	- milestone4.md
	- makefile
	- conf.py

# Distribution of Code:
PyPI

# License Selection:
GNU Lesser General Public License v3.0 or later
