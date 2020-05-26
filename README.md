# pathfinder.vim

An experimental Vim plugin based on [this Reddit post][reddit].

Taking a cursor start position and an end position, it uses Dijkstra's
algorithm to find most efficient combination of motions to move between them.
This can be used to discover new ways of doing things, which is especially
helpful for beginners who are not familiar with the options available.

There is also a possibility of extending the script in the future to work with
other types of edits, such as operators, macros, marks and so on.

## Installation

Use your favorite plugin manager. I recommend
[vim-plug](https://github.com/junegunn/vim-plug).

## Usage

1. `:PathfinderBegin` with your cursor over the starting position
2. Move to the ending position (within the same buffer) using whatever
   inefficient method you like
1. `:PathfinderRun` with your cursor on the end position

Note that long-distance movements can take a while to process.

## Configuration

The plugin uses two global variables for the supported motions:

```vim
let g:pf_motions = [
  \ {'motion': 'j', 'weight': 2, 'rweight': 1},
  \ {'motion': 'k', 'weight': 2, 'rweight': 1},
  \ {'motion': 'gj', 'weight': 3, 'rweight': 1},
  \ {'motion': 'gk', 'weight': 3, 'rweight': 1},
  \ ...
  \ ]
let g:pf_motions_target_line_only = [
  \ {'motion': '0', 'weight': 1, 'rweight': 1},
  \ {'motion': '^', 'weight': 1, 'rweight': 1},
  \ {'motion': 'g^', 'weight': 2, 'rweight': 1},
  \ {'motion': '$', 'weight': 1, 'rweight': 1},
  \ ...
  \ ]
```

`g:pf_motions` contains motions which can be used to move between lines (these
may also work within the current line).
`g:pf_motions_target_line_only` contains motions which may only be used once
the cursor has reached same line as the target, e.g. `h`, `^`, `g_`. This
blocks the algorithm from trying to move diagonally across the file.

`weight` sets the cost of using each motion, and `rweight` sets the cost of
each time it is repeated after that. Setting `rweight` lower than `weight`
means that it is preferred to repeat the same motion again than to use two
different motions.

The weights in the default settings are just the number of keypresses to perform
the motion, with 1 added to everything in `g:pf_motions` (so that movements from
`g:pf_motions_target_line_only` are used when there is a choice between two
with the same effect). `rweight` is set to 1 for everything.


[reddit]: https://www.reddit.com/r/vim/comments/gpam7f/plugin_to_suggest_how_to_be_more_efficient/frm01tx?utm_source=share&utm_medium=web2x
