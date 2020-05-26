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
  let b:pf_start = winsaveview()
  echom 'Move to target location and then :PathfinderRun'
endfunction
command PathfinderBegin call PathfinderBegin()


function! CreateNode(view, rb, rf)
  let g = (has_key(a:rf, 'reached_by') && a:rf.reached_by == a:rb)
        \ ? a:rb.rweight : a:rb.weight
  return {'key': a:view.lnum . ',' . a:view.col,
        \ 'view': a:view,
        \ 'g': a:rf.g + g,
        \ 'reached_by': a:rb,
        \ 'reached_from': a:rf}
endfunction

function! DoMotion(node, child_nodes, motion)
  call winrestview(a:node.view)
  try
    execute 'silent! normal! ' . a:motion.motion
  catch
    " Ignore motions which cause an error
    return
  endtry

  if winsaveview().lnum != a:node.view.lnum || winsaveview().col != a:node.view.col
    " Only add the child node if the motion had an effect
    " This means we don't add things such as l at the end of a line
    call add(a:child_nodes, CreateNode(winsaveview(), a:motion, a:node))
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
  if !exists('b:pf_start')
    echom 'Please run :PathfinderBegin to set a start position first'
    return
  endif

  let b:pf_target = winsaveview()

  let closed_nodes = {}
  let open_nodes = {}
  let motion_sequence = []

  let start_node = {'key': b:pf_start.lnum . ',' . b:pf_start.col,
                   \ 'view': b:pf_start, 'g': 0}
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

    " We don't want to compare the scroll position
    if current_node.view.lnum == b:pf_target.lnum && current_node.view.col == b:pf_target.col
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

  call winrestview(start_node.view)
  redraw
  if len(motion_sequence)
    call EchoKeys(motion_sequence)
  else
    echom 'No path found'
  endif
endfunction
command PathfinderRun call PathfinderRun()
