#!/bin/bash

current_branch=$(git branch | head -n 1)

if [ "$current_branch" != "* book" ]; then
    echo "Please checkout the sparkletop.github.io book branch: git checkout book"
    exit 1
fi

# Clean symlinks from previous builds
rm tex/media/*

# Clean auxillary tex files from previous builds
./clean-tex-aux.fish

# Parse the docs and generate the main tex
python mkdocsparse.py . ./tex/chapters.tex

# Compile the pdf
cd tex
latexmk -xelatex -latexoption="-shell-escape" -f template.tex
cd ..