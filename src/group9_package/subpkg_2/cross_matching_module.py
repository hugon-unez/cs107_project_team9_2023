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
            result_dataframe = cross_match_module.cross_match(10, 1237671939275162601)
            print(result_dataframe)
        """

        try:
                # Construct the query string using f-string
                query = f"SELECT original_ext_source_id, angular_distance FROM gaiadr3.sdssdr13_best_neighbour WHERE original_ext_source_id = {sourceid}"

                # Execute the query using astroquery.gaia
                job = Gaia.launch_job(query)
                results = job.get_results()

                # Convert results to a pandas DataFrame
                df = results.to_pandas()

                # Filter results based on angular distance upper bound
                pure_df = df[df['angular_distance'] <= angular_distance_max]

                return pure_df

        except astropy.utils.exceptions.TimeoutError:
            print("Query timed out. Please try again later.")
        except astropy.utils.exceptions.RemoteServiceError:
            print("Remote service error. Please check your internet connection.")
        except Exception as e:
            print(f"An error occurred: {e}")


