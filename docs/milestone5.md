As a group, we discussed the SRS clarifications that were given to us for this milestone and came to the conclusion that we did not need to update how the modules, classes, and functions interact with eachother, and therefore there was no need to make any changes to the diagram demonstrating how these parts interact. We confirmed this plan with Victor, of whom is our liason for this project. 

However, in our API_draft folder, we did edit our README.md file to clarify how the modules are going to be implemented given the SRS clarifications. 

Specifically, for Annex A: 3.A - we made edits to how data preprocessing is going to be applied. This change to our implementation ensures that each function is applied to each spectrum independently and preserves the data. In regard to adaptability and usability, this change allows an adaptable function to a wide range of spectral data which we may not have encountered before. With regards to enhanced functionality, the increases in adaptability inherently increase the functionality. For data preprocessing, ensuring data quality through these changes allows other modules to use this preprocessed data as intended.

For Annex 3.B: our updates to include the class label ensures that each row has a label. Adding more data makes a more adaptable and usable table for different purposes. Some of these purposes include machine learning classification and visualization. This adaptability increases the integration, since our machine learning module will be classifiying based on label. Without this change, we would not a functional machine learning module, highlighting the importance of this change.

Finally, for Annex 3.C, we clarified the return type for our function. By ensuring we return flux, this enables the wavelength align function to be better used in conjunction with other functions, increasing integration with visualization module specifically. Additionally, the wavelength align module becomes more more user friendly with the presented clarifications, since it is more clear to the user how to use this function.

modules to be evaluated for integration:
- core_functions_module_extract
- core_functions_module_modify

