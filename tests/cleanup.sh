#!/bin/sh

find . -name '*.pyc' -exec rm -f {} \; 2>/dev/null
find . -name tmp-files -type dir -exec rm -rf {} \; 2>/dev/null
