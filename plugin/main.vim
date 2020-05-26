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


function! PathfinderBegin()
  " Record the current cursor position
  let w:pf_start_line = line('.')
  let w:pf_start_col = virtcol('.')
endfunction
command PathfinderBegin call PathfinderBegin()


function! CoordString(l, c)
  return a:l . ',' . a:c
endfunction

function! CreateNode(l, c, rb, rf)
  let key = CoordString(a:l, a:c)
  let g = (has_key(a:rf, 'reached_by') && a:rf.reached_by == a:rb)
        \ ? a:rb.rweight : a:rb.weight
  return {'key': key, 'line': a:l, 'col': a:c, 'g': a:rf.g + g,
        \ 'reached_by': a:rb, 'reached_from': a:rf}
endfunction

function! DoMotion(node, child_nodes, motion)
  call cursor(a:node.line, a:node.col)
  try
    execute 'silent! normal! ' . a:motion.motion
  catch
    " Ignore motions which cause an error
    return
  endtry

  if line('.') != a:node.line || virtcol('.') != a:node.col
    " Only add the child node if the motion had an effect
    " This means we don't add things such as l at the end of a line
    call add(a:child_nodes, CreateNode(line('.'), virtcol('.'), a:motion, a:node))
  endif
endfunction

function! GetChildNodes(node)
  let child_nodes = []
  for motion in g:pf_motions
    call DoMotion(a:node, child_nodes, motion)
  endfor
  return child_nodes
endfunction

function! Backtrack(final_node)
  let node = a:final_node
  let motion_sequence = []
  while has_key(node, 'reached_from')
    call add(motion_sequence, node.reached_by.motion)
    let node = node.reached_from
  endwhile

  call reverse(motion_sequence)
  return motion_sequence
endfunction

function! EchoKeys(motion_sequence)
  " Combine repeated motions into one with a count
  " Basically run length encoding
  let motion_string = ''
  let last_motion = ''
  let c = 0
  for motion in a:motion_sequence
    if last_motion !=# motion
      let motion_string = motion_string . (c > 1 ? c : '') . last_motion
      let last_motion = motion
      let c = 1
    else
      let c = c + 1
    endif
  endfor
  let motion_string = motion_string . (c > 1 ? c : '') . last_motion

  echom motion_string
endfunction

function! PathfinderRun()
  if !exists('w:pf_start_line') || !exists('w:pf_start_col')
    echom 'Please run :PathfinderBegin to set a start position first'
    return
  endif

  let w:pf_end_line = line('.')
  let w:pf_end_col = virtcol('.')
  let initial_view = winsaveview()

  let closed_nodes = {}
  let open_nodes = {}
  let motion_sequence = []

  let start_node = {'key': CoordString(w:pf_start_line, w:pf_start_col),
                   \ 'line': w:pf_start_line, 'col': w:pf_start_col, 'g': 0}
  let open_nodes[start_node.key] = start_node

  while len(open_nodes) > 0
    " Find the node with the lowest value of g
    let current_node = values(open_nodes)[0]
    for node in values(open_nodes)
      if node.g < current_node.g
        let current_node = node
      endif
    endfor
    " Remove from open set
    unlet open_nodes[current_node.key]
    let closed_nodes[current_node.key] = current_node

    if current_node.line == w:pf_end_line && current_node.col == w:pf_end_col
      " Found the target
      let motion_sequence = Backtrack(current_node)
      break
    endif

    for child_node in GetChildNodes(current_node)
      if has_key(closed_nodes, child_node.key) | continue | endif

      if has_key(open_nodes, child_node.key)
	      " Replace the existing node if this one has a lower g
      	if child_node.g < open_nodes[child_node.key].g
	        call extend(open_nodes[child_node.key], child_node)
      	endif
      else
        let open_nodes[child_node.key] = child_node
      endif
    endfor
  endwhile

  call winrestview(initial_view)
  redraw
  if len(motion_sequence)
    call EchoKeys(motion_sequence)
  else
    echom 'No path found'
  endif
endfunction
command PathfinderRun call PathfinderRun()
