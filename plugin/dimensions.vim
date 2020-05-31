" Get the width of the current window, excluding sign and number columns
function! WindowTextWidth()
  let l:decorationColumns = &number ? &numberwidth : 0

  if has('folding')
    let l:decorationColumns += &foldcolumn
  endif

  if has('signs')
    if &signcolumn ==? 'yes' || &signcolumn ==? 'number'
      " Sign column is always enabled
      let l:decorationColumns += 2
    elseif &signcolumn ==? 'auto'
      redir => l:signs
      silent execute 'sign place buffer=' . bufnr('')
      redir END

      " The output of the command above contains two header lines
      " Any more and that means signs are displayed
      if len(split(l:signs, "\n")) > 2
	  let l:decorationColumns += 2
      endif
    endif
  endif

  return winwidth(0) - l:decorationColumns
endfunction
