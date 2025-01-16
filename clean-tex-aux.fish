#!/usr/bin/fish

cd tex
set files *.{aux,log,fdb_latexmk,fls,out,pyg,synctex.gz,pdf,toc,lof,lol,xdv}
rm -f $files
rm -rf _minted-template
cd ..