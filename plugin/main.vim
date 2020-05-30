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
  " Importing this will spawn a new, barebones Vim process to act as the
  " server, and do other setup steps
  python3 from client import client

  function! PollResponses(timer)
    python3 client.poll_responses()
  endfunction
  let s:timer = timer_start(100, 'PollResponses', {'repeat': -1})

  augroup CloseServerOnQuit
    autocmd!
    autocmd VimLeave * call timer_stop(s:timer)
    autocmd VimLeave * python3 client.close()
  augroup END

  " Bind commands to Python functions
  python3 from commands import pathfinder_begin, pathfinder_run
  command! PathfinderBegin python3 pathfinder_begin()
  command! PathfinderRun python3 pathfinder_run()
endif


let g:pf_loaded = 1
