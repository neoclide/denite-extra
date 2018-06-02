" ============================================================================
" Description: Commands of session
" Author: Qiming Zhao <chemzqm@gmail.com>
" Licence: MIT licence
" Version: 0.1
" Last Modified:  June 02, 2018
" ============================================================================

if exists('g:loaded_session')
  finish
endif
let g:loaded_session = 1

let g:session_directory = get(g:, 'session_directory', expand('~').'/.vim/sessions')
let s:restart_cmd = expand('<sfile>:h:h').'/bin/nvimstart'

function! s:RestartVim() abort
  " TODO use neoclide
  if exists('g:nyaovim_version')
    call rpcnotify(0, 'nyaovim:reload')
    return
  elseif has('gui_running') && has('gui_macvim')
    let cmd = 'mvim'
  elseif has('gui_running')
    let cmd = 'gvim'
  else
    let cmd = 'vim'
  endif
  let name = empty(v:this_session) ? 'default' : v:this_session
  call session#save(name)
  if exists(':ItermStart') && has('gui_running')
    let succeed = Iterm#Run(cmd . ' -c "SessionLoad ' . name . '"')
    if !succeed | return | endif
  elseif has('nvim')
    call jobstart(s:restart_cmd . ' ' . v:this_session , {
      \ 'detach': 1,
      \})
  else
    silent execute '!' . cmd . ' -c "SessionLoad ' . v:this_session . '"'
    if v:shell_error| return | endif
  endif
  silent! wa
  silent quitall!
endfunction

command! -nargs=? -complete=customlist,session#complete
      \ SessionSave call session#save(<q-args>)

command! -nargs=? -complete=customlist,session#complete
      \ SessionLoad call session#load(<q-args>)

command! -nargs=0 RestartVim call s:RestartVim()
