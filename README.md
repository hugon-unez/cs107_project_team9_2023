# CS107 Final Project - Team 9
[![CS107 Project - Code Coverage](https://code.harvard.edu/CS107/team09_2023/actions/workflows/coverage.yml/badge.svg?branch=dev)](https://code.harvard.edu/CS107/team09_2023/actions/workflows/coverage.yml)

[![CS107 Project - Tests](https://code.harvard.edu/CS107/team09_2023/actions/workflows/tests.yml/badge.svg?branch=dev)](https://code.harvard.edu/CS107/team09_2023/actions/workflows/tests.yml)


Paul Alexis Self-Eval:
I spent approximately a total of 20 hours on the project. The bulk of this was dedicated to figuring things out as opposed to actually writing the code. My main contributions to the project include the initial api mapping, the data-preprocessing module, the unit tests for the preprocessing module, the crossmatch module and description of the execution of our first package. As a less experienced coder on the team, I was given a bit of runway to work on the modules, which may have led to spending more time on modules than someone with more experience would have done. It also meant that some of my initial work had to be tweaked by the team.

Ricardo Linares' Self-Eval:
I spent approximately a total of 50 hours on the project. Roughly 6 hours of this time was spent on Milestones 3 and 4, deciding how our team was going to organize the modules and detailing this in the API_draft, and milestone4.md file. Roughly 8 hours of this time was spent on configuring the yml files and debugging them. About 8 hours was spent coding and testing the machine learning module, as I was the sole coder of this module and its tests. The rest of the 28 hours were spent on things such as (1) creating docstrings for code and tests that did not have them and revising the docstrings to make them more detailed for code that did have them; (2) making integration tests for the visualize module, the SpectraExtract Class of the core_functions_module_extract module, and unit tests for the SpectraExtract Class of the core_functions_module_extract module and the WavelengthAlignment Class of the core_functions_module_modify module; (3) and lastly making the html files for our documentation.

Zachary Stack Self-Eval: 
I worked on this project approximately 45-50 hours on a many different aspects. My main contributions were troubleshooting and developing the continuous integration ymls, working on the unit tests and integration tests for both the extract and modify module, working on fixing up the DataPreprocessing module, writing the tests for the DataPreprocessing module with patching, developing the DataAugmentation module and tests with that module, and writing the tests for the visualization module. When working with the ymls, I worked with Ricardo and Hugo in person for 8 hours to get the scripts to run and learned a great deal once we were successful in running. Also, I worked on zoom with Paul to troubleshoot with our TF Victor and helped with Paul’s modules since I have some experience coding. Finally, I helped prepare the notebook which demonstrated our notebook. I tried to touch every aspect in this project to try to learn as much as possible and took as many of the tests as possible since I do not have much industry experience with them. 

Sameer Das Self-Eval: 
I spent approximately 18-20 hours working on this project. I spent most of my time focusing on creating the metadata extraction shaping and ensuring that we could access data in the proper shapes/frames in order to operate in other functions. I spent a few hours earlier on in the project with helping organize the module structure. Later on in the project, my contributions were helping with documentation issues we had with SDSS sourcing and then making sure we could hit the SRS targets for certain labels such as classification of star/galaxy. Other than this, I lended a hand on making suggestions for direction of various aspects of data augmentation (didn't write any code, just made suggestions) and adding some portions of code here and there. 

How to Run tests:
- enter the tests folder
- run the script by running "./run_tests.sh pytest" in the command line
