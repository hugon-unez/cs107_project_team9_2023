from astroquery.gaia import Gaia
import pandas as pd
import requests
import astropy

import ssl
# must fix ssl error
ssl._create_default_https_context = ssl._create_unverified_context

class CrossMatchingModule:
    def __init__(self):
        pass

    def cross_match(self, angular_distance_max, sourceid):
        """
        Performs a cross-match query between Gaia and SDSS data, filtering the results 
        by a specified maximum angular distance.

        This method queries the Gaia dr3 archieve for objects that match an input Gaia 
        source ID within the SDSS catalog. The function returns a pandas DataFrame containing 
        the angular distance and the corresponding external source ID from SDSS, if the angular
        distance is below the threshold.

        Args:
            angular_distance_max (float): The maximum angular distance in arcsec used 
                                        to filter the cross-match results. Only objects 
                                        with an angular distance less than or equal to 
                                        this threshold will be returned.
            sourceid (int): The Gaia source ID for which the cross-match is to be performed.

        Returns:
            pandas.DataFrame: A DataFrame containing two columns: 'original_ext_source_id' 
                            and 'angular_distance'. The single row represents an object from 
                            SDSS that matches the specified Gaia source ID within the 
                            given angular distance.

        Raises:
            Exception: If there is an error in executing the query or in data retrieval.

        Example:
            cross_match_module = CrossMatchingModule()
            result_dataframe = cross_match_module.cross_match(10, 6279435494640163584)
            print(result_dataframe)
        """

        try:
            # Ensure there are inputs
            if angular_distance_max is None or sourceid is None:
                raise TypeError("Input values cannot be None")

            # Convert inputs to integers and validate
            angular_distance_max = float(angular_distance_max)
            sourceid = int(sourceid)

            if angular_distance_max < 0:
                raise ValueError("Angular distance must be a non-negative integer")

            query = f"SELECT original_ext_source_id, angular_distance FROM gaiadr3.sdssdr13_best_neighbour WHERE source_id = {sourceid}"
            job = Gaia.launch_job(query)
            results = job.get_results()
            df = results.to_pandas()
            pure_df = df[df['angular_distance'] <= angular_distance_max]
            return pure_df

        except ValueError as ve:
            print(f"Input error: {ve}")
            raise
        except TypeError as te:
            print(f"Type error: {te}")
            raise
        except requests.exceptions.HTTPError as he:
            print(f"HTTP error occurred: {he}")
            raise requests.exceptions.HTTPError
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

