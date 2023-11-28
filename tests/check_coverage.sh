#!/usr/bin/env bash
# File       : check_coverage.sh
# Description: Coverage wrapper around test suite driver script
# Copyright 2022 Harvard University. All Rights Reserved.
coverage_threshold=90
coverage_result=$(coverage run --source=group9_package -m pytest && coverage report --fail-under=$coverage_threshold)
echo "$coverage_result"