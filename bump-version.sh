#!/bin/bash

version=$1
sed -i -e "s/^\([[:blank:]]*__version__ = \).*/\1'$version'/" sphinx_lua/version.py
git add sphinx_lua/version.py
git commit  -m "bump version to $version"
git tag $version
git push
git push origin $version
