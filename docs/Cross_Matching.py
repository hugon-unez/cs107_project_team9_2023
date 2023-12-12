from astroquery.gaia import Gaia
from astroquery.sdss import SDSS
import pandas as pd

class CrossMatchingModule:
    def __init__(self, gaia_query, sdss_query):
        self.gaia_query = gaia_query
        self.sdss_query = sdss_query

    def cross_match(self):
        # Query Gaia
        gaia_job = Gaia.launch_job(self.gaia_query)
        gaia_results = gaia_job.get_results()
        gaia_data = gaia_results.to_pandas()

        # Query SDSS
        sdss_job = SDSS.query_sql(self.sdss_query)
        sdss_data = sdss_job.to_pandas()

        # Perform Cross-Matching. How do we know what columns to merge on? Just have ra as placeholder but unsure
        merged_data = pd.merge(gaia_data, sdss_data, how='inner', on='ra' )

        # Example: Keep only matches with a certain magnitude difference
        magnitude_difference_threshold = 0.1
        filtered_data = merged_data[abs(merged_data['gaia_magnitude'] - merged_data['sdss_magnitude']) < magnitude_difference_threshold]

        return filtered_data