highlight default link PathfinderPopup Cursor

if !exists('g:pf_autorun_delay')
  let g:pf_autorun_delay = 2
endif

if !exists('g:pf_popup_time')
  let g:pf_popup_time = 3000
endif

if !exists('g:pf_explore_scale')
  let g:pf_explore_scale = 0.5
endif
if !exists('g:pf_max_explore')
  let g:pf_max_explore = 10
endif

if !exists('g:pf_descriptions')
  let g:pf_descriptions = {
    \ 'h': 'Left {count} columns',
    \ 'l': 'Right {count} columns',
    \ 'j': 'Down {count} lines',
    \ 'k': 'Up {count} lines',
    \ 'gj': 'Down {count} display lines',
    \ 'gk': 'Up {count} display lines',
    \ 'gg': 'To the start of the buffer',
    \ 'G': 'To the end of the buffer',
    \ 'H': 'To line {count} from the top of the window',
    \ 'M': 'To the middle of the window',
    \ 'L': 'To line {count} from the bottom of the window',
    \ '': 'Scroll downward {count} lines',
    \ '': 'Scroll upward {count} lines',
    \ '': 'Scroll forward {count} pages',
    \ '': 'Scroll backward {count} pages',
    \ '': 'Scroll downward {count} times',
    \ '': 'Scroll upward {count} times',
    \ 'zt': 'Current line to the top of the window',
    \ 'z\': 'Current line to the top of the window and move to the first non-blank character',
    \ 'zz': 'Current line to the centre of the window',
    \ 'z.': 'Current line to the centre of the window and move to the first non-blank character',
    \ 'zb': 'Current line to the bottom of the window',
    \ 'z-': 'Current line to the bottom of the window and move to the first non-blank character',
    \ '0': 'To the start of the line',
    \ '^': 'To the first non-blank character on the line',
    \ 'g^': 'To the first non-blank character on the display line',
    \ '$': 'To the end of the line',
    \ 'g$': 'To the end of the display line',
    \ 'g_': 'To the last non-blank character on the line',
    \ 'gm': 'To the centre of the screen',
    \ 'gM': 'To the centre of the line',
    \ 'W': '{count} WORDs forward (inclusive)',
    \ 'E': 'Forward to the end of WORD {count} (exclusive)',
    \ 'B': '{count} WORDs backward (inclusive)',
    \ 'gE': 'Backward to the end of WORD {count} (exclusive)',
    \ 'w': '{count} words forward (inclusive)',
    \ 'e': 'Forward to the end of word {count} (exclusive)',
    \ 'b': '{count} words backward (inclusive)',
    \ 'ge': 'Backward to the end of word {count} (exclusive)',
    \ '(': '{count} sentences backward',
    \ ')': '{count} sentences forward',
    \ '{': '{count} paragraphs backward',
    \ '}': '{count} paragraphs forward',
    \ ']]': '{count} sections forward or to the next { in the first column',
    \ '][': '{count} sections forward or to the next } in the first column',
    \ '[[': '{count} sections backward or to the previous { in the first column',
    \ '[]': '{count} sections backward or to the previous } in the first column',
    \ ']m': '{count} next start of a method (Java or similar)',
    \ '[m': '{count} previous start of a method (Java or similar)',
    \ ']M': '{count} next end of a method (Java or similar)',
    \ '[M': '{count} previous end of a method (Java or similar)',
    \ '*': 'Search forward for occurrence {count} of the word nearest to the cursor',
    \ '#': 'Search backward for occurrence {count} of the word nearest to the cursor',
    \ 'g*': 'Search forward for occurrence {count} of the word nearest to the cursor, allowing matches which are not a whole word',
    \ 'g#': 'Search backward for occurrence {count} of the word nearest to the cursor, allowing matches which are not a whole word',
    \ '%': 'Go to the matching bracket',
    \ 'f': 'To occurrence {count} of "{argument}", to the right',
    \ 't': 'Till before occurrence {count} of "{argument}", to the right',
    \ 'F': 'To occurrence {count} of "{argument}", to the left',
    \ 'T': 'Till after occurrence {count} of "{argument}", to the left',
    \ '/': 'Search forwards for occurence {count} of "{argument}"',
    \ '?': 'Search backwards for occurence {count} of "{argument}"',
    \ }
endif
