# pathfinder.vim

A Vim plugin to give suggestions to improve your movements.
It's a bit like [Clippy][office-assistant].

[![Demo](https://asciinema.org/a/CYX4I94GGBsHZqMVc9N8MerFD.svg)](https://asciinema.org/a/CYX4I94GGBsHZqMVc9N8MerFD)

[office-assistant]: https://en.wikipedia.org/wiki/Office_Assistant


## Features

- Automatic suggestions for cursor movements
- Help summaries to aid in understanding
- Asynchronous - pathfinding runs in a separate process


## Installation

Use your favorite plugin manager. I recommend
[vim-plug](https://github.com/junegunn/vim-plug).

```vim
if has('python3') && has('timers')
  Plug 'danth/pathfinder.vim'
else
  echoerr 'pathfinder.vim is not supported on this Vim installation'
endif
```

You may also need to run `git submodule update --init` from inside the plugin
directory. Most popular plugin managers will do that automatically.


## Usage

1. Move the cursor in normal, visual or visual-line mode.
2. That's it.

Suggestions pop up above the cursor if you have:

- Vim 8.2 or above, with `+popupwin`
- Neovim 0.4 or above

Otherwise, they will appear as a plain `echo` at the bottom of the screen.

### Explanations

If you don't understand how a suggestion works, you should use the
`:PathfinderExplain` command, which will show a short description of each
motion used.

If you find yourself using this a lot, make a mapping for it!

```vim
noremap <leader>pe :PathfinderExplain<CR>
```

### Manual Commands

If you set [`g:pf_autorun_delay`](#gpf_autorun_delay) to a negative value,
you get two commands instead:

- `:PathfinderBegin`: Set the start position. This still happens automatically
  when switching windows/tabs, or loading a new file.
- `:PathfinderRun`: Set the target position and get a suggestion.


## Related Plugins

- [vim-be-good](https://github.com/ThePrimeagen/vim-be-good) - Various training games to practice certain actions
- [vim-hardtime](https://github.com/takac/vim-hardtime) - Prevent yourself from repeating keys like `h`,`j`,`k`,`l`


## Configuration

*pathfinder.vim works out-of-the box with the default configuration. You don't
need to read this section if you don't want to.*

### `highlight PathfinderPopup`
Change the appearance of suggestion popups. *Default: same as cursor*

### `g:pf_popup_time`
Milliseconds to display the popup for. *Default: 3000*

### `g:pf_autorun_delay`
When this number of seconds have elapsed with no motions being made, the
pathfinder will run. It also runs for other events such as changing modes.
A negative value will disable automatic suggestions. *Default: 2*

### `g:pf_explore_scale`
Multiplier which determines the range of lines to be explored around the start
and target positions. This is calculated as (lines between start and target
&times; multiplier) and added to both sides. *Default: 0.5*

This limitation improves performance by disallowing movements outside the area
of interest. It also prevents suggestions which rely on knowing about the exact
text hundreds of lines away. Settings below 1 cause movements within a line to
only use motions inside that line.

If you have a powerful computer, you can increase this option to a high value
to allow exploring more of the file. You can also disable it completely by
setting a negative value.

### `g:pf_max_explore`
Cap the number of surrounding lines explored (see above) to a maximum value.
As usual, this can be disabled by making it negative. *Default: 10*

### `g:pf_descriptions`
Dictionary of descriptions, used for `:PathfinderExplain`.

```vim
let g:pf_descriptions['k'] = 'Up {count} lines'
let g:pf_descriptions['f'] = 'To occurence {count} of "{argument}", to the right'
```

Ensure the plugin is loaded before trying to override keys.  Otherwise, the
default dictionary will not exist and you'll get an error.

Re-defining the entire dictionary is not recommended since it could cause
problems if support for a new motion is added and you don't have a description
for it.
