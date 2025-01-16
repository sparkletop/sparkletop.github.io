#!/bin/bash 

cd tex
latexmk -xelatex -latexoption="-shell-escape" -f template.tex
cd ..