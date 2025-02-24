#!/bin/bash

cd tex
files="*.aux *.log *.fdb_latexmk *.fls *.out *.pyg *.synctex.gz *.pdf *.toc *.lof *.lol *.xdv *.bbl *.bcf *.blg *.run.xml *-SAVE-ERROR"
rm -f $files
rm -rf _minted/*
rm -rf chapters/*.aux