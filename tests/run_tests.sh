#!/usr/bin/env bash
# File       : run_tests.sh
# Description: Test suite driver script
# Copyright 2022 Harvard University. All Rights Reserved.
set -e

# list of test cases you want to run
tests=(
    subpkg_1/test_core_functions_module_extract.py
    subpkg_1/test_visualize.py
    subpkg_1/test_unittests_core_function_module.py
    subpkg_1/test_unittests_core_function_modify.py
)

# Must add the module source path because we use `import group9_package` in
# our test suite.  This is necessary if you want to test in your local
# development environment without properly installing the package.
export PYTHONPATH="$(pwd -P)/../src":${PYTHONPATH}

# decide what driver to use (depending on arguments given)
if [[ $# -gt 0 && ${1} == 'coverage' ]]; then
    driver="${@} -m unittest"
elif [[ $# -gt 0 && ${1} == 'pytest' ]]; then
    driver="${@}"
elif [[ $# -gt 0 && ${1} == 'CI' ]]; then
    # Assumes the package has been installed and dependencies resolved.  This
    # would be the situation for a customer.  Uses `pytest` for testing.
    shift
    unset PYTHONPATH
    driver="pytest ${@}"
else
    driver="python ${@} -m unittest"
fi

# run the tests
${driver} ${tests[@]}