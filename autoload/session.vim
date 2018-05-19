let s:save_cpo = &cpo
set cpo&vim
let s:is_win = has('win32') || has('win64')

function! session#save(filename, ...)
  if !isdirectory(g:session_directory)
    call mkdir(g:session_directory, 'p')
  endif

  let filename = s:get_session_path(a:filename)

  " Check if this overrides an existing session
  if filereadable(filename) && a:0 && a:1
    echoerr 'Session already exists.'
    return
  endif

  execute 'silent mksession!' filename

  echohl MoreMsg
  echo 'Saved session: ' . fnamemodify(v:this_session, ':t:r')
  echohl None
endfunction

function! session#load(filename)
  let filename = s:get_session_path(a:filename)
  if !filereadable(filename)
    call unite#sources#session#_save(filename)
    return
  endif

  noautocmd silent! %bwipeout!
  execute 'silent! source' filename

  for bufnr in range(1, bufnr('$'))
    call setbufvar(bufnr, '&modified', 0)
  endfor
endfunction

function! session#complete(A, C, P)
  return map(split(glob(g:session_directory.'/*.vim'), "\n"), "fnamemodify(v:val, ':t:r')")
endfunction

function! s:get_session_path(filename)
  let filename = a:filename
  if filename == ''
    let filename = v:this_session
  endif
  if filename == ''
    let filename = 'default'
  endif

  if filename !~ '.vim$'
    let filename .= '.vim'
  endif

  if filename !~ '^\%(/\|\a\+:/\)'
    " Relative path.
    let filename = get(g:, 'denite_source_session_path', s:home().'/session') . '/' . filename
  endif

  return filename
endfunction

function! s:home()
  if s:is_win
    return $VIM."/vimfiles"
  endif
  return $HOME."/.vim"
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
