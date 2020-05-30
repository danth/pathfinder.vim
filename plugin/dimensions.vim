" Get the width of the current window, excluding sign and number columns
function! WindowTextWidth()
  let decorationColumns = &number ? &numberwidth : 0

  if has('folding')
    let decorationColumns += &foldcolumn
  endif

  if has('signs')
    if &signcolumn ==? 'yes' || &signcolumn ==? 'number'
      " Sign column is always enabled
      let decorationColumns += 2
    elseif &signcolumn ==? 'auto'
      redir => signs
      silent execute 'sign place buffer=' . bufnr('')
      redir END

      " The output of the command above contains two header lines
      " Any more and that means signs are displayed
      if len(split(signs, "\n")) > 2
	  let decorationColumns += 2
      endif
    endif
  endif

  return winwidth(0) - decorationColumns
endfunction
