#!/bin/bash

current_branch=$(git branch | head -n 1)

if [ "$current_branch" != "* book" ]; then
    echo "Please checkout the sparkletop.github.io book branch: git checkout book"
    exit 1
fi

# Remove symlinks from previous builds
rm tex/media/*

# Parse the docs and generate the main tex
./m2t.sh

# Compile the pdf
./t2p.sh