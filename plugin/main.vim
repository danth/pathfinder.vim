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


if exists('g:pf_server_communication_file')
  " Importing this will run the server and connect back to the client
  python3 import pathfinder.server.server
else
  python3 from pathfinder.client.plugin import Plugin; plugin = Plugin()

  command! PathfinderBegin python3 plugin.command_begin()
  command! PathfinderRun python3 plugin.command_run()
  command! PathfinderExplain python3 plugin.command_explain()

  function! PathfinderLoop(timer)
    " Check for responses from the server
    python3 plugin.client.poll_responses()
    " Check if we should take any actions automatically
    python3 plugin.autorun()
  endfunction

  if !exists("s:timer")
    let s:timer = timer_start(100, 'PathfinderLoop', {'repeat': -1})
  endif
  augroup PathfinderStopOnLeave
    autocmd!
    autocmd VimLeave * call timer_stop(s:timer)
    autocmd VimLeave * python3 plugin.stop()
  augroup END
endif


let g:pf_loaded = 1
