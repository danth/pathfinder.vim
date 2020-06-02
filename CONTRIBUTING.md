# Contributing to Pathfinder.vim

*This file contains information about the inner workings of pathfinder.vim.
You should also read these [general contributing guidelines][default-contributing].*

[default-contributing]: https://github.com/AlphaMycelium/.github/blob/master/CONTRIBUTING.md

## Development environment

The plugin files will be cloned somewhere under `~/.vim` by your plugin manager.
For example Plug places them in `~/.vim/plugged/pathfinder.vim/`.

Some plugin managers also allow you to clone the repository into a directory of
your choice and use the path to that directory to install the plugin.

## Pathfinding

The pathfinding algorithm used for motions is [Dijkstra's algorithm][dijkstra],
which is just a greedy algorithm. It is extended to use an additional "refining"
step after the path has been found, which chooses between congruent motions
(two or more motions which go from and to the same location).

[dijkstra]: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

## Python to Vim interface

Vim (when compiled with `+python3`) comes with an embedded Python module called
`vim`, which is used to send commands and output from Python.

In Vimscript, the following syntax is used to call Python code:

```vim
python3 <line of code>
```

```vim
python3 << endpython
<multiple lines of code>
endpython
```

## Client and Server

The way we discover connections between nodes (characters) in the pathfinding
graph is:

1. Move the cursor to the node position
2. Run the motion with `silent! normal! <motion>`
3. Check where the cursor moved to and record it as a connection

This causes the cursor to move around while things are being tested. We want to
allow users to continue working while paths are found, hence we start a "server"
which is basically another Vim process using [this barebones vimrc](serverrc.vim).

The user's Vim (the client) sends the contents of the current buffer, the start
and target positions, the window dimensions and some other information to the
server when it wants to request a path. This communication happens through
`multiprocessing.connection` with a temporary file.

The server will then do pathfinding in the background and send the result back
when it is done, which the client receives and displays.
