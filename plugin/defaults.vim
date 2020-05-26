if !exists('g:pf_motions')
  let g:pf_motions = [
    \ {'motion': 'h', 'weight': 1, 'rweight': 1},
    \ {'motion': 'l', 'weight': 1, 'rweight': 1},
    \ {'motion': 'j', 'weight': 1, 'rweight': 0.1},
    \ {'motion': 'k', 'weight': 1, 'rweight': 0.1},
    \ {'motion': 'gj', 'weight': 2, 'rweight': 1},
    \ {'motion': 'gk', 'weight': 2, 'rweight': 1},
    \
    \ {'motion': 'gg', 'weight': 2, 'rweight': 1},
    \ {'motion': 'G', 'weight': 1, 'rweight': 1},
    \
    \ {'motion': '0', 'weight': 1, 'rweight': 1},
    \ {'motion': '^', 'weight': 1, 'rweight': 1},
    \ {'motion': 'g^', 'weight': 2, 'rweight': 1},
    \ {'motion': '$', 'weight': 1, 'rweight': 1},
    \ {'motion': 'g$', 'weight': 2, 'rweight': 1},
    \ {'motion': 'g_', 'weight': 2, 'rweight': 1},
    \
    \ {'motion': 'W', 'weight': 1, 'rweight': 1},
    \ {'motion': 'E', 'weight': 1, 'rweight': 1},
    \ {'motion': 'B', 'weight': 1, 'rweight': 1},
    \ {'motion': 'gE', 'weight': 2, 'rweight': 1},
    \ {'motion': 'w', 'weight': 1, 'rweight': 1},
    \ {'motion': 'e', 'weight': 1, 'rweight': 1},
    \ {'motion': 'b', 'weight': 1, 'rweight': 1},
    \ {'motion': 'ge', 'weight': 2, 'rweight': 1},
    \
    \ {'motion': '(', 'weight': 1, 'rweight': 1},
    \ {'motion': ')', 'weight': 1, 'rweight': 1},
    \ {'motion': '{', 'weight': 1, 'rweight': 1},
    \ {'motion': '}', 'weight': 1, 'rweight': 1},
    \ {'motion': ']]', 'weight': 2, 'rweight': 1},
    \ {'motion': '][', 'weight': 2, 'rweight': 1},
    \ {'motion': '[[', 'weight': 2, 'rweight': 1},
    \ {'motion': '[]', 'weight': 2, 'rweight': 1},
    \ {'motion': ']m', 'weight': 2, 'rweight': 1},
    \ {'motion': '[m', 'weight': 2, 'rweight': 1},
    \
    \ {'motion': '#', 'weight': 1, 'rweight': 1},
    \ {'motion': '*', 'weight': 1, 'rweight': 1},
    \ {'motion': '%', 'weight': 1, 'rweight': 1},
    \ ]
endif
