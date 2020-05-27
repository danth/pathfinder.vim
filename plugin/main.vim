function! PathfinderBegin()
  let b:pf_start = winsaveview()
  echom 'Move to target location and then :PathfinderRun'
endfunction
command! PathfinderBegin call PathfinderBegin()


" Loop backwards through the path from a:node to the start
" and call a:function for each except the start node
" If the function returns 1 then the loop will be broken
function! s:Backtrack(node, function)
  let current_node = a:node
  while has_key(current_node, 'reached_from')
    if a:function(current_node) | break | endif
    let current_node = current_node.reached_from
  endwhile
endfunction

function! s:CalcGIncrement(node)
  " Count how many times the reached_by motion has been repeated
  let s:repetition_count = 0
  let s:ginc_node = a:node
  function! s:RepetitionCounter(node)
    if a:node.reached_by == s:ginc_node.reached_by
      let s:repetition_count += 1
    else | return 1 | endif
  endfunction
  call s:Backtrack(a:node, function('s:RepetitionCounter'))

  let g = s:GetGIncrementFromCount(a:node, s:repetition_count)
  unlet s:repetition_count s:ginc_node
  return g
endfunction

function! s:GetGIncrementFromCount(node, repetition_count)
  " If the count is 1 (first time used), return the set weight of the motion
  if a:repetition_count == 1 | return a:node.reached_by.weight | endif

  " Otherwise, return how many characters the count has increased in length by
  " e.g. 2 -> 3 is 0, 9 -> 10 is 1, 1 -> 100 would be 2
  if a:repetition_count == 2
    return 1 " 2 is a special case since 1 can be omitted
  endif
  return len(a:repetition_count) - len(a:repetition_count - 1)
endfunction

function! s:CreateNode(view, rb, rf)
  let node = {'key': a:view.lnum . ',' . a:view.col,
            \ 'view': a:view,
            \ 'reached_by': a:rb,
            \ 'reached_from': a:rf}
  let node.g = a:rf.g + s:CalcGIncrement(node)
  return node
endfunction

function! s:DoMotion(node, motion)
  call winrestview(a:node.view)
  try
    execute 'silent! normal! ' . a:motion.motion
  catch | return {} | endtry

  if winsaveview().lnum != a:node.view.lnum || winsaveview().col != a:node.view.col
    " Only return the child node if the motion moved the cursor
    return s:CreateNode(winsaveview(), a:motion, a:node)
  else
    return {}
  endif
endfunction

function! s:EchoKeys(final_node)
  let s:motions = []
  let s:last_motion = ''
  let s:c = 0
  function! s:AddToMotionString(node)
    if s:last_motion !=# a:node.reached_by.motion
      call add(s:motions, (s:c > 1 ? s:c : '') . s:last_motion)
      let s:last_motion = a:node.reached_by.motion
      let s:c = 1
    else | let s:c += 1 | endif
  endfunction

  call s:Backtrack(a:final_node, function('s:AddToMotionString'))
  call add(s:motions, (s:c > 1 ? s:c : '') . s:last_motion)

  " Reverse to get the motions in the right order
  echom join(reverse(s:motions), '')

  unlet s:motions s:last_motion s:c
endfunction

function! PathfinderRun()
  if !exists('b:pf_start')
    echom 'Please run :PathfinderBegin to set a start position first'
    return
  endif

  let b:pf_target = winsaveview()

  let closed_nodes = {}
  let open_nodes = {}

  let start_node = {'key': b:pf_start.lnum . ',' . b:pf_start.col,
                   \ 'view': b:pf_start, 'g': 0}
  let open_nodes[start_node.key] = start_node

  let final_node = {}

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

    " If we reach the target node, break
    " We don't want to compare the scroll position so must check line and
    " column individually
    if current_node.view.lnum == b:pf_target.lnum
      \ && current_node.view.col == b:pf_target.col
      let final_node = current_node
      break
    endif

    for motion in g:pf_motions
      let child_node = s:DoMotion(current_node, motion)
      if child_node == {} || has_key(closed_nodes, child_node.key) | continue | endif

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
  if final_node == {} | echom 'ERROR: No path found'
  else | call s:EchoKeys(final_node) | endif
endfunction
command! PathfinderRun call PathfinderRun()
