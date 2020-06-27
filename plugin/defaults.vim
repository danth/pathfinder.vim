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

if !exists('g:pf_motions')
  let g:pf_motions = [
    \ {'motion': 'h', 'weight': 1, 'description': 'Left {count} columns'},
    \ {'motion': 'l', 'weight': 1, 'description': 'Right {count} columns'},
    \ {'motion': 'j', 'weight': 1, 'description': 'Down {count} lines'},
    \ {'motion': 'k', 'weight': 1, 'description': 'Up {count} lines'},
    \ {'motion': 'gj', 'weight': 2, 'description': 'Down {count} display lines'},
    \ {'motion': 'gk', 'weight': 2, 'description': 'Up {count} display lines'},
    \
    \ {'motion': 'gg', 'weight': 2, 'description': 'To the start of the buffer'},
    \ {'motion': 'G', 'weight': 1, 'description': 'To the end of the buffer'},
    \
    \ {'motion': 'H', 'weight': 1, 'description': 'To line {count} from the top of the window'},
    \ {'motion': 'M', 'weight': 1, 'description': 'To the middle of the window'},
    \ {'motion': 'L', 'weight': 1, 'description': 'To line {count} from the bottom of the window'},
    \ {'motion': '\<C-f>', 'name': 'CTRL-f', 'weight': 1, 'description': 'Scroll forward {count} pages'},
    \ {'motion': '\<C-b>', 'name': 'CTRL-b', 'weight': 1, 'description': 'Scroll backward {count} pages'},
    \ {'motion': '\<C-d>', 'name': 'CTRL-d', 'weight': 1, 'description': 'Scroll downward {count} times'},
    \ {'motion': '\<C-u>', 'name': 'CTRL-u', 'weight': 1, 'description': 'Scroll upward {count} times'},
    \
    \ {'motion': '0', 'weight': 1, 'description': 'To the start of the line'},
    \ {'motion': '^', 'weight': 1, 'description': 'To the first non-blank character on the line'},
    \ {'motion': 'g^', 'weight': 2, 'description': 'To the first non-blank character on the display line'},
    \ {'motion': '$', 'weight': 1, 'description': 'To the end of the line'},
    \ {'motion': 'g$', 'weight': 2, 'description': 'To the end of the display line'},
    \ {'motion': 'g_', 'weight': 2, 'description': 'To the last non-blank character on the line'},
    \ {'motion': 'gm', 'weight': 2, 'description': 'To the centre of the screen'},
    \ {'motion': 'gM', 'weight': 2, 'description': 'To the centre of the line'},
    \
    \ {'motion': 'W', 'weight': 1, 'description': '{count} WORDs forward (inclusive)'},
    \ {'motion': 'E', 'weight': 1, 'description': 'Forward to the end of WORD {count} (exclusive)'},
    \ {'motion': 'B', 'weight': 1, 'description': '{count} WORDs backward (inclusive)'},
    \ {'motion': 'gE', 'weight': 2, 'description': 'Backward to the end of WORD {count} (exclusive)'},
    \ {'motion': 'w', 'weight': 1, 'description': '{count} words forward (inclusive)'},
    \ {'motion': 'e', 'weight': 1, 'description': 'Forward to the end of word {count} (exclusive)'},
    \ {'motion': 'b', 'weight': 1, 'description': '{count} words backward (inclusive)'},
    \ {'motion': 'ge', 'weight': 2, 'description': 'Backward to the end of word {count} (exclusive)'},
    \
    \ {'motion': '(', 'weight': 1, 'description': '{count} sentences backward'},
    \ {'motion': ')', 'weight': 1, 'description': '{count} sentences forward'},
    \ {'motion': '{', 'weight': 1, 'description': '{count} paragraphs backward'},
    \ {'motion': '}', 'weight': 1, 'description': '{count} paragraphs forward'},
    \ {'motion': ']]', 'weight': 2, 'description': '{count} sections forward or to the next { in the first column'},
    \ {'motion': '][', 'weight': 2, 'description': '{count} sections forward or to the next } in the first column'},
    \ {'motion': '[[', 'weight': 2, 'description': '{count} sections backward or to the previous { in the first column'},
    \ {'motion': '[]', 'weight': 2, 'description': '{count} sections backward or to the previous } in the first column'},
    \ {'motion': ']m', 'weight': 2, 'description': '{count} next start of a method (Java or similar)'},
    \ {'motion': '[m', 'weight': 2, 'description': '{count} previous start of a method (Java or similar)'},
    \ {'motion': ']M', 'weight': 2, 'description': '{count} next end of a method (Java or similar)'},
    \ {'motion': '[M', 'weight': 2, 'description': '{count} previous end of a method (Java or similar)'},
    \
    \ {'motion': '*', 'weight': 1, 'description': 'Search forward for occurrence {count} of the word nearest to the cursor'},
    \ {'motion': '#', 'weight': 1, 'description': 'Search backward for occurrence {count} of the word nearest to the cursor'},
    \ {'motion': 'g*', 'weight': 2, 'description': 'Search forward for occurrence {count} of the word nearest to the cursor, allowing matches which are not a whole word'},
    \ {'motion': 'g#', 'weight': 2, 'description': 'Search backward for occurrence {count} of the word nearest to the cursor, allowing matches which are not a whole word'},
    \ {'motion': '%', 'weight': 1, 'description': 'Go to the matching bracket'},
    \
    \ {'motion': 'f', 'weight': 2, 'description': 'To occurrence {count} of "{char}", to the right'},
    \ {'motion': 't', 'weight': 2, 'description': 'Till before occurrence {count} of "{char}", to the right'},
    \ {'motion': 'F', 'weight': 2, 'description': 'To occurrence {count} of "{char}", to the left'},
    \ {'motion': 'T', 'weight': 2, 'description': 'Till after occurrence {count} of "{char}", to the left'},
    \ ]
endif
