from astroquery.gaia import Gaia
import pandas as pd

class CrossMatchingModule:
    def __init__(self):
        pass

    def cross_match(self, angular_distance_max, sourceid):
        # Define the table name
        table_name = 'sdssdr13_best_neighbour'

        # Construct the query string using f-string
        query = f"SELECT angular_distance, original_ext_source_id FROM {table_name} WHERE source_id = {sourceid}"

        # Execute the query using astroquery.gaia
        job = Gaia.launch_job(query)
        results = job.get_results()

        # Convert results to a pandas DataFrame
        df = pd.DataFrame(results)

        # Filter results based on angular distance upper bound
        pure_df = df[df['angular_distance'] <= angular_distance_max]

        return pure_df

# Example usage:
cross_match_module = CrossMatchingModule()
angular_distance_upper_bound = 2.0
#Example source id
source_id_to_query = 123456789  
result_dataframe = cross_match_module.cross_match(angular_distance_upper_bound, source_id_to_query)

# Display the result
print(result_dataframe)
