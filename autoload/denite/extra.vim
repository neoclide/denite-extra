
function! denite#extra#feedkeys(keys, ...)
  let pre = get(a:, 1, ':')
  function! Callback(key, pre, id)
    call feedkeys(a:pre . a:key . "", 'n')
  endfunction
  call timer_start(100, function('Callback', [a:keys, pre]))
endfunction

function! denite#extra#search(keys)
  function! Callback(key, id)
    call feedkeys('/' . a:key . "\<CR>", 'n')
  endfunction
  call timer_start(100, function('Callback', [a:keys]))
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

function! s:osascript(...) abort
  let args = join(map(copy(a:000), '" -e ".shellescape(v:val)'), '')
  let output = system('osascript'. args)
  if v:shell_error && output !=# ""
    echohl Error | echon output | echohl None
    return
  endif
endfunction

function! s:escape(filepath)
  return "'".substitute(a:filepath, "'", "\\'", 'g')."'"
endfunction
