let s:save_cpo = &cpo
set cpo&vim

function! password#list()
  let old_cwd = getcwd()
  lcd ~/.password-store
  let l:list = systemlist('ag -g .')
  execute 'lcd '.old_cwd
  call filter(l:list, 'v:val !~ "README"')
  call map(l:list, "substitute(v:val, '.gpg$', '', '')")
  return l:list
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
