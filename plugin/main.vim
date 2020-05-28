if !has('python3')
  echom 'The +python3 feature is required to run pathfinder.vim'
  finish
endif
if exists('g:pf_loaded') | finish | endif


python3 << endpython
import vim
import sys
from os.path import normpath, join

plugin_root_dir = vim.eval("fnamemodify(resolve(expand('<sfile>:p')), ':h')")
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)

from commands import *
endpython


function! PathfinderBegin()
  let b:pf_start = winsaveview()
  echom 'Move to target location and then :PathfinderRun'
endfunction
command! PathfinderBegin call PathfinderBegin()

function! PathfinderRun()
  if !exists('b:pf_start')
    echom 'Please run :PathfinderBegin to set a start position first'
    return
  endif

  python3 pathfinder_run()
endfunction
command! PathfinderRun call PathfinderRun()


let g:pf_loaded = 1
