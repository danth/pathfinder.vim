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


" Get a list of items which the two lists have in common
function! IntersectLists(list1, list2)
  let result = copy(a:list1)
  call filter(result, 'index(a:list2, v:val) >= 0')
  return result
endfunction


" Calculate how much a:node.g should increase based on information from
" previous nodes
function! s:CalcGIncrement(node)
  " Count how many times the incoming motion has been repeated
  let s:repetition_count = 0
  let s:ginc_node = a:node
  function! s:RepetitionCounter(node)
    if len(IntersectLists(a:node.incoming_motions,
                        \ s:ginc_node.incoming_motions))
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
  if a:repetition_count == 1 | return a:node.incoming_motions[0].weight | endif

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
            \ 'reached_from': a:rf,
            \ 'incoming_motions': [a:rb]}
  let node.g = a:rf.g + s:CalcGIncrement(node)
  return node
endfunction


" Test the a:motion from a:node, and return a new child node if the cursor
" moves
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


" Backtrack and select the best choices from each node.incoming_motions
function! s:RefinePath(final_node)
  " Build a 2d list where each item is a list of the possible congruent
  " motions which can be used there
  let s:motion_options = []
  function! s:AddToMotionOptions(node)
    call add(s:motion_options, a:node.incoming_motions)
  endfunction
  call s:Backtrack(a:final_node, function('s:AddToMotionOptions'))
  " Backtracking builds the list in reverse order, so we need to flip it
  " around
  call reverse(s:motion_options)

  function! s:GetBestMotionFromTriplet(left, centre, right)
    if len(a:centre) == 1 | return a:centre[0] | endif

    " Look for motions we have in common with either side
    let l_c = IntersectLists(a:left, a:centre)
    let c_r = IntersectLists(a:centre, a:right)

    if len(l_c) > 1 || len(c_r) > 1
      " Look for motions we have in common with *both* sides
      let l_c_r = IntersectLists(l_c, c_r)
      if len(l_c_r) > 0 | return l_c_r[0] | endif
    endif

    if len(c_r) > 0 | return c_r[0] | endif
    if len(l_c) > 0 | return l_c[0] | endif
    return a:centre[0]
  endfunction

  " Select the best motion from each sub-list, such that we can combine as
  " many together with counts as possible
  " e.g. 3} is preferred over j2} where the first j and } have the same effect
  let motions = []
  let i = 0
  while i < len(s:motion_options)
    let left = i > 0 ? s:motion_options[i-1] : []
    let right = i < len(s:motion_options)-1 ? s:motion_options[i+1] : []
    call add(motions, s:GetBestMotionFromTriplet(left, s:motion_options[i], right))
    let i += 1
  endwhile

  unlet s:motion_options
  return motions
endfunction

" Call s:RefinePath and then print it in a human-readable format
function! s:EchoKeys(final_node)
  let motions = s:RefinePath(a:final_node)

  " Combine repeated motions using counts
  let motion_string = ''
  let last_motion = ''
  let c = 0
  for motion in motions
    if last_motion !=# motion.motion
      let motion_string .= (c > 1 ? c : '') . last_motion
      let last_motion = motion.motion
      let c = 1
    else | let c += 1 | endif
  endfor
  let motion_string .= (c > 1 ? c : '') . last_motion

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
        " There is already a node in the same position, update it
      	if child_node.g == open_nodes[child_node.key].g
          \ && child_node.reached_from == open_nodes[child_node.key].reached_from
          " This is an alternative motion with the same g value,
          " add it to the list
          call add(open_nodes[child_node.key].incoming_motions, motion)
        elseif child_node.g < open_nodes[child_node.key].g
          " This is a shorter route, discard the old ones
          call extend(open_nodes[child_node.key], child_node)
      	endif
      else
        " Add new node
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
