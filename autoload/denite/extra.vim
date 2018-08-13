
function! denite#extra#feedkeys(keys, ...)
  let s:keys = a:keys
  if !exists('*timer_start')
    echohl Error | echon 'timer_start requires for feedkeys to work' | echohl None
  else
    function! Callback(id)
      call feedkeys(s:keys . "", 'n')
    endfunction
    call timer_start(100, function('Callback'))
  endif
endfunction

function! denite#extra#search(keys)
  let s:keys = a:keys
  function! Callback(...)
    call feedkeys('/' . s:keys . "\<CR>", 'n')
  endfunction
  call timer_start(100, function('Callback'))
endfunction

function! denite#extra#iterm_tabopen(dir)
  call s:osascript(
    \ 'tell application "iTerm2"',
    \   'tell current window',
    \     'create tab with default profile',
    \     'tell current session',
    \       'delay 0.1',
    \       'write text "cd '.s:escape(a:dir).'"',
    \       'write text "clear"',
    \     'end tell',
    \   'end tell',
    \ 'end tell')
endfunction

function! denite#extra#iterm_tabrun(dir, cmd)
  call s:osascript(
    \ 'tell application "iTerm2"',
    \   'tell current window',
    \     'create tab with default profile',
    \     'tell current session',
    \       'delay 0.1',
    \       'write text "cd '.s:escape(a:dir).'"',
    \       'write text "clear"',
    \       'write text "'.a:cmd.'"',
    \     'end tell',
    \   'end tell',
    \ 'end tell')
endfunction

function! s:osascript(...) abort
  let args = join(map(copy(a:000), '" -e ".shellescape(v:val)'), '')
  let output = system('osascript'. args)
  if v:shell_error && output !=# ""
    echohl Error | echon output | echohl None
    return
  endif
endfunction

function! denite#extra#cc(index)
  call timer_start(60, { -> execute('cc! '.a:index)})
endfunction

function! s:escape(filepath)
  return "'".substitute(a:filepath, "'", "\\'", 'g')."'"
endfunction
