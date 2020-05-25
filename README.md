# pathfinder.vim

An experimental Vim plugin based on [this Reddit post][reddit]. Taking a start
position and an end position, it attempts to calculate the best combination of
motions in order to move between them.

## Installation

Use your favorite plugin manager. I recommend
[vim-plug](https://github.com/junegunn/vim-plug).

## Usage

1. `:PathfinderBegin` with your cursor over the starting position
2. Move to the ending position (within the same window and buffer) using
   whatever inefficient method you like
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

`g:pf_motions` contains motions which can be used to move between or along lines.
`g:pf_motions_target_line_only` contains motions restricted to once the cursor
is on the same line as the target, e.g. `h`, `^`, `g_`. This prevents the
pathfinder from trying to move diagonally, as well as other weird bugs.

`weight` sets the cost of using the motion, and subsequently `rweight` sets the
cost for each time it is repeated. These values can be tuned to get the best
results.

The defaults for `weight` are the number of characters typed to perform the
motion, with 1 added to everything in `g:pf_motions` (so that movements from
`g:pf_motions_target_line_only` are chosen when there is a tie between two
which have the same effect). `rweight` is set to 1 for everything.


[reddit]: https://www.reddit.com/r/vim/comments/gpam7f/plugin_to_suggest_how_to_be_more_efficient/frm01tx?utm_source=share&utm_medium=web2x
