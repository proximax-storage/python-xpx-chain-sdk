#!/bin/bash

VERSION=$1

sed -i "s/release = '.*'/release = \'${VERSION}\'/" doc/conf.py
sed -i "s/version = .*/version = ${VERSION}/" setup.cfg
sed -i "s/release = .*/release = ${VERSION}/" setup.cfg
sed -i "s/VERSION = \".*\"/VERSION = \"${VERSION}\"/" setup.py

grep -n "${VERSION}" setup.py setup.cfg doc/conf.py

git diff setup.py setup.cfg doc/conf.py
