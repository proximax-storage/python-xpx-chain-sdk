#!/bin/bash

# Delete all logging imports and logger calls
for F in `grep -r "import logging" * | grep "\.py" | grep -v "$0" | grep -v "build/lib" | grep -v "\.swp" | sed 's/\(.*\):.*/\1/'`; do 
    sed -i '/import logging/d' $F
    sed -i '/logging.basicConfig/d' $F
    sed -i '/logger =/d' $F
    sed -i '/logger\./d' $F
done
