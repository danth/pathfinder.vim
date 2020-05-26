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

The plugin uses a global variable which lists the supported motions:

```vim
let g:pf_motions = [
  \ {'motion': 'h', 'weight': 1, 'rweight': 1},
  \ {'motion': 'l', 'weight': 1, 'rweight': 1},
  \ {'motion': 'j', 'weight': 1, 'rweight': 0.1},
  \ {'motion': 'k', 'weight': 1, 'rweight': 0.1},
  \ ...
  \ ]
```

`weight` sets the cost of using each motion, and `rweight` sets the cost of
each time it is repeated after that. Setting `rweight` lower than `weight`
means that it is preferred to repeat the same motion again than to use two
different motions.

The weights in the default settings are just the number of keypresses to perform
the motion. `rweight` is set to 1 for almost everything.


[reddit]: https://www.reddit.com/r/vim/comments/gpam7f/plugin_to_suggest_how_to_be_more_efficient/frm01tx?utm_source=share&utm_medium=web2x

## Related Plugins

- [vim-be-good](https://github.com/ThePrimeagen/vim-be-good) - Various training games to practice certain actions
- [vim-hardtime](https://github.com/takac/vim-hardtime) - Prevent yourself from repeating keys like `h`,`j`,`k`,`l`
