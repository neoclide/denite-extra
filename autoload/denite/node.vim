
function! denite#node#update(cmd, path, cwd)
  let old_cwd = getcwd()
  execute 'lcd ' . a:cwd
  if exists('*termopen')
    execute 'belowright 5new'
    set winfixheight
    call termopen(a:cmd, {
          \ 'on_exit': function('s:OnUpdate'),
          \ 'source_path': a:path,
          \ 'buffer_nr': bufnr('%'),
          \})
    call setbufvar('%', 'is_autorun', 1)
    execute 'wincmd p'
  else
    execute '!'.a:cmd
  endif
  execute 'lcd ' . old_cwd
endfunction

function! s:OnUpdate(job_id, status, event) dict
  if a:status == 0
    execute 'silent! bd! '.self.buffer_nr
    let content = json_decode(join(readfile(self.source_path . '/package.json'), ''))
    echohl WarningMsg | echon 'Updated '.content.name.' to '.content.version | echohl None
  endif
endfunction
