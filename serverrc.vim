set nocompatible

" Disable unnecessary features
set noruler
set nonumber
set noshowcmd
set signcolumn=no
filetype off
syntax off

" Add pathfinder.vim to runtimepath
let &runtimepath = fnamemodify(resolve(expand('<sfile>:p')), ':h')
