if exists('g:pf_loaded') | finish | endif
if !has('python3')
  echom 'The +python3 feature is required to run pathfinder.vim'
  finish
endif
if !has('timers')
  echom 'The +timers feature is required to run pathfinder.vim'
  finish
endif


python3 << endpython
import vim
import sys
from os.path import normpath, join

plugin_root_dir = vim.eval("fnamemodify(resolve(expand('<sfile>:p')), ':h')")
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
endpython


if exists('g:pf_server_communiation_file')
  " Importing this will run the server and connect back to the client
  python3 import server
else
  python3 import commands

  " Set up a timer to call the loop function peroidically
  function! PathfinderLoop(timer)
    python3 commands.loop()
  endfunction
  augroup PathfinderStartOnEnter
    autocmd!
    autocmd VimEnter * let s:timer = timer_start(100, 'PathfinderLoop', {'repeat': -1})
  augroup END

  " Stop the loop and call the stop function on VimLeave
  augroup PathfinderStopOnLeave
    autocmd!
    autocmd VimLeave * call timer_stop(s:timer)
    autocmd VimLeave * python3 commands.stop()
  augroup END

  " Bind events to Python functions
  augroup PathfinderEventBindings
    autocmd!
    autocmd WinEnter,TabEnter,BufNewFile,BufReadPre,SessionLoadPost * python3 commands.reset()
  augroup END
endif


let g:pf_loaded = 1
