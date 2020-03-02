#!/bin/bash

for F in `python setup.py flake8 2>/dev/null | grep "\.py" | sed 's/:.*:.*:.*//' | uniq`; do
    # Remove starting whitespaces on empty lines
    sed -i -r 's/^\s+$//' $F

    # Remove trailing whitespaces
    sed -i -r 's/\s+$//' $F
done

for F in `python setup.py flake8_tests 2>/dev/null | grep "\.py" | sed 's/:.*:.*:.*//' | uniq`; do
    # Remove starting whitespaces on empty lines
    sed -i -r 's/^\s+$//' $F

    # Remove trailing whitespaces
    sed -i -r 's/\s+$//' $F
done

python setup.py flake8
python setup.py flake8_tests
