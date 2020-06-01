#!/usr/bin/env bash

export PYTHONPATH=.

# check for pep8/pycodestyle compliance
pycodestyle ./*.py --show-source --ignore=E501,E116

pycodestyle_exit=$?

# if not compliant, exit
if [ $pycodestyle_exit -ne 0 ]
then exit $pycodestyle_exit
fi

# run tests
coverage run -m pytest

pytest_exit=$?

coverage report -m

exit $pytest_exit