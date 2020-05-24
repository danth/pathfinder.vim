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
  \ {'motion': 'j', 'weight': 1},
  \ {'motion': 'k', 'weight': 1},
  \ {'motion': '(', 'weight': 2},
  \ {'motion': ')', 'weight': 2},
  \ ...
  \ ]
let g:pf_motions_target_line_only = [
  \ {'motion': '0', 'weight': 2},
  \ {'motion': '^', 'weight': 2},
  \ {'motion': '$', 'weight': 2},
  \ {'motion': 'g_', 'weight': 3},
  \ ...
  \ ]
```

`g:pf_motions` contains motions which can be used to move between or along lines.
`g:pf_motions_target_line_only` contains motions restricted to once the cursor
is on the same line as the target, e.g. `h`, `^`, `g_`. This prevents the
pathfinder from trying to move diagonally, as well as other weird bugs.

`weight` sets the cost of each time the motion is used, and can be tuned to get
the best results. The defaults are mainly based on the number of characters
typed and the complexity of the motion (more complex = harder to remember).


[reddit]: https://www.reddit.com/r/vim/comments/gpam7f/plugin_to_suggest_how_to_be_more_efficient/frm01tx?utm_source=share&utm_medium=web2x
