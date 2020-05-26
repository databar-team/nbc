#!/usr/bin/env bash

export PYTHONPATH=.

pycodestyle ./*.py --show-source --ignore=E501,E116

# sleep 120

coverage run -m pytest

testExit=$?

coverage report -m

exit $testExit