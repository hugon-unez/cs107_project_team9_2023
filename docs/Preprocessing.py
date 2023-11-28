#Importing Libraries and original Base class
from core_functions_module import SpectralAnalysisBase
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import zscore
from astropy.table import Table
from astroquery.sdss import SDSS

class DataPreprocessor(SpectralAnalysisBase):
#Spectral Data:
#Definition: Spectral data represents how the intensity of light emitted or received 
#by an object varies across different wavelengths. Representation: A spectrum is often 
#presented as a graph where the x-axis represents the wavelength (or frequency) of light
#and the y-axis represents the intensity or flux of light at each wavelength.

#Flux in the context of spectra refers to the intensity of light at each wavelength. 
#It quantifies how much energy is emitted or received by an object per unit of time,
#Per unit of area, and per unit of wavelength

#For light waves, the wavelength corresponds to the distance between two successive 
#peaks or troughs of the electromagnetic wave.


#Don't have to worry about query since the user is expected to provide the query
    def __init__(self, query_flux, query_wavelength):
        #So here, am i establishing flux as the query from the original class?
        super().__init__(query_flux)
        self.query_wavelength = query_wavelength

        #1.Based on the original base class, does query_flux and query_wavelength have to be table names?

    def normalize_data(self):
        if self.data is not None:
            # Perform normalization on flux data in PhotoObjAll
            #2.I'm not sure which table I am supposed to be pulling flux data from. How would I know the column name?
            #Getting Z Score of flux data
            normalized_flux_data = (self.data['flux'] - np.mean(self.data['flux'])) / np.std(self.data['flux'])
            
            #Resetting what the column is equal to
            self.data['flux'] = normalized_flux_data
        else:
            raise ValueError("No flux data available for normalization")

    def remove_outliers(self, threshold=2.5):
        if self.data is not None:
            # Remove outliers from flux data in PhotoObjAll using z-score
            z_scores = np.abs(zscore(self.data['flux']))
            outliers_removed_data = self.data[z_scores < threshold]
            self.data = outliers_removed_data
        else:
            raise ValueError("No flux data available for outlier removal")

#Interpolation is commonly employed when you have a set of discrete data points 
#and you want to estimate the values at positions that are not explicitly provided.
    def interpolate_data(self, new_wavelengths):
        if self.data is not None:
            # Interpolate flux data in PhotoObjAll to new_wavelengths
            interpolate_U = interp1d(self.data_wavelength['u'], self.data['flux'], kind='linear', fill_value='extrapolate')(new_wavelengths)
            
            #Interpolating flux and wavelength and then replacing
            self.data = Table({'u': new_wavelengths, 'flux': interpolate_flux})
        else:
            raise ValueError("No flux data available for interpolation")


#the light emitted by distant objects undergoes a redshift, meaning that the wavelengths of the 
#Emitted light are stretched and shifted towards the longer, "red" end of the electromagnetic spectrum.

#the redshift of an object is directly proportional to its distance from an observer due to the expansion 
# of the universe. The farther an object is, the greater its redshift tends to be.



#Where do I get the redshift values??


#Can I do self.data_wavelength?

#How do I access the wavelength column?
    def correct_redshift(self, redshift_values):
        if self.data_wavelength is not None:
            # Adjust wavelengths in SpecObjAll based on redshift values
            self.data_wavelength['wavelength'] /= (1 + redshift_values)
        else:
            raise ValueError("No wavelength data available for redshift correction")