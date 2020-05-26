function! PathfinderBegin()
  let b:pf_start = winsaveview()
  echom 'Move to target location and then :PathfinderRun'
endfunction
command! PathfinderBegin call PathfinderBegin()


function! CalcGIncrement(node)
  " Count how many times the reached_by motion has been repeated
  let current_node = a:node
  let repetition_count = 0
  while current_node.reached_by == a:node.reached_by
    let repetition_count += 1
    let current_node = current_node.reached_from

    if !has_key(current_node, 'reached_by')
      break " We reached the start node
    endif
  endwhile

  " If the count is 1 (first time used), return the set weight of the motion
  if repetition_count == 1 | return a:node.reached_by.weight | endif

  " Otherwise, return how many characters the count has increased in length by
  " e.g. 2 -> 3 is 0, 9 -> 10 is 1, 1 -> 100 would be 2
  if repetition_count == 2
    return 1 " 2 is a special case since 1 can be omitted
  endif
  return len(repetition_count) - len(repetition_count - 1)
endfunction

function! CreateNode(view, rb, rf)
  let node = {'key': a:view.lnum . ',' . a:view.col,
            \ 'view': a:view,
            \ 'reached_by': a:rb,
            \ 'reached_from': a:rf}
  let node.g = a:rf.g + CalcGIncrement(node)
  return node
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
command! PathfinderRun call PathfinderRun()
