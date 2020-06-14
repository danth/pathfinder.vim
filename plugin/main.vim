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

plugin_root = vim.eval("fnamemodify(resolve(expand('<sfile>:p')), ':h')")
sys.path.insert(0, normpath(join(plugin_root, '..')))
sys.path.insert(0, normpath(join(plugin_root, '..', 'heapdict')))
endpython


if exists('g:pf_server_communiation_file')
  " Importing this will run the server and connect back to the client
  python3 import pathfinder.server.server
else
  python3 from pathfinder.client import commands

  " Manual commands to be used when autorun is disabled
  command! PathfinderBegin python3 commands.reset()
  command! PathfinderRun python3 commands.update_current(); commands.run()

  " Set up a timer to call the loop function peroidically
  function! PathfinderLoop(timer)
    " Check for responses from the server
    python3 commands.client.poll_responses()

    if g:pf_autorun_delay > 0
      " Only autorun if user has enabled it
      python3 commands.autorun()
    endif
  endfunction
  augroup PathfinderStartOnEnter
    autocmd!
    autocmd VimEnter * let s:timer = timer_start(100, 'PathfinderLoop', {'repeat': -1})
  augroup END

  " Stop the loop and call the stop function on VimLeave
  augroup PathfinderStopOnLeave
    autocmd!
    autocmd VimLeave * if exists('s:timer') | call timer_stop(s:timer) | endif
    autocmd VimLeave * python3 commands.stop()
  augroup END

  " Bind events to Python functions
  augroup PathfinderEventBindings
    autocmd!
    autocmd WinEnter,TabEnter,BufNewFile,BufReadPre,SessionLoadPost * python3 commands.reset()
  augroup END
endif


let g:pf_loaded = 1
