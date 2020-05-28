# pathfinder.vim

An experimental Vim plugin based on [this Reddit post][reddit].

Taking a cursor start position and an end position, it uses Dijkstra's
algorithm to find the most optimal combination of motions to move between
them. This can be used to discover new ways of doing things, which is
especially helpful for beginners who are not familiar with the options
available.

There is also a possibility of extending the script in the future to work with
other types of edits, such as operators, macros, marks and so on.

[reddit]: https://www.reddit.com/r/vim/comments/gpam7f/plugin_to_suggest_how_to_be_more_efficient/frm01tx?utm_source=share&utm_medium=web2x

## Installation

Use your favorite plugin manager. I recommend
[vim-plug](https://github.com/junegunn/vim-plug).

```vim
Plug 'AlphaMycelium/pathfinder.vim'
```

pathfinder.vim requires Vim to be compiled with the `+python3` feature.

```vim
:echo has('python3')
```

## Usage

1. Place your cursor on a starting position.
2. Run `:PathfinderBegin`.
3. Move the cursor to another position (within the same buffer).
4. Use `:PathfinderRun` to see the most optimal set of movements you should
   have used in step 3.

Note that long-distance movements can take a while to process.

Your cursor will return to the starting position, which gives you a chance to
practice the optimal motion. Learn by usage!

## Configuration

*pathfinder.vim works out-of-the box with the default configuration. You don't
need to read this section if you don't want to.*

The plugin uses a global variable to set the available motions:

```vim
let g:pf_motions = [
  \ {'motion': 'h', 'weight': 1},
  \ {'motion': 'l', 'weight': 1},
  \ {'motion': 'j', 'weight': 1},
  \ {'motion': 'k', 'weight': 1},
  \ ...
  \ ]
```

This contains all the supported motions by default, so you only need to change
it if you want to adjust the weighting or delete some of them.

Each motion has a weight associated with it. The higher the weight, the less
the pathfinding algorithm wants to use that motion. The path with the lowest
total weight wins. The default settings use the number of characters in the
motion as its weight.

However, repeating a motion will not use its predefined weight. Instead, the
cost is calculated based on the effect adding another repetition will have on
the string length of the count. This is easier to explain with examples:

| Motion | Cost of adding the repetition |
| --- | --- |
| `j` | (uses configured weight) |
| `j` -> `2j` | 1, since the `2` has been added |
| `2j` -> `3j` | 0, because `3j` is no longer than `2j` |
| `9j` -> `10j` | 1, since `10j` is a character longer than `9j` |
| `1j` -> `100j` | 2, since `100j` is 2 characters longer than `1j` |

It is recommended that the only modifications you make to the list are:

- Increasing the weight of motions you don't like
- Deleting motions you never want to use
- Changing the order of motions to put the ones you prefer first

## Related Plugins

- [vim-be-good](https://github.com/ThePrimeagen/vim-be-good) - Various training games to practice certain actions
- [vim-hardtime](https://github.com/takac/vim-hardtime) - Prevent yourself from repeating keys like `h`,`j`,`k`,`l`
