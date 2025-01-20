#!/bin/bash 

cd tex
latexmk -lualatex -latexoption="-shell-escape" -f template.tex
cd ..