#!/bin/bash 

rm tex/media/*
python mkdocsparse.py . tex/chapters.tex tex/frontmatter.tex