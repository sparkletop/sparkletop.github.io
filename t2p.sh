#!/bin/bash 

latexmk -pdflua -latexoption="-shell-escape" -bibtex -cd tex/template.tex