from setuptools import setup, find_packages

# Your classifiers as a list of strings
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: OS Independent",
]

setup(
    name="team09CS107Harvard2023",
    version="0.0.7",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=classifiers, 
)
