# Denite-extra

[![](http://img.shields.io/github/issues/neoclide/denite-extra.svg)](https://github.com/neoclide/denite-extra/issues)
[![](http://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![](https://img.shields.io/badge/doc-%3Ah%20denite--extra.txt-red.svg)](doc/denite-extra.txt)

Some extra sources for [denite.nvim](https://github.com/Shougo/denite.nvim).

_Related projects:_

* [denite-git](https://github.com/neoclide/denite-git) git log, status and changed
  lines source for denite.nvim
* [ultisnips](https://github.com/neoclide/ultisnips) ultisnips fork with
  denite.nvim support
* [redismru.vim](https://github.com/neoclide/redismru.vim) support redismru
  source of denite.nvim
* [todoapp.vim](https://github.com/neoclide/todoapp.vim) support todo source of
  denite.nvim
* [macnote.vim](https://github.com/neoclide/macnote.vim) support note source of
  denite.nvim

## Install

Take [vim-plug](https://github.com/junegunn/vim-plug) for example, add:

    Plug 'Shougo/denite.nvim'
    Plug 'chemzqm/denite-extra'

To your `.vimrc` and run `PlugInstall` and `UpdateRemotePlugins` after
restarted.

**Note:** [denite.nvim](https://github.com/Shougo/denite.nvim) requires python3+
so make sure `has('python3')` return true, and run:

    pip3 install neovim

before you install any neovim remote plugin.

Run `:CheckHealth` if you get any problem.

**Note:** `tabopen` action of this source is for `iTerm2` tab, which is Mac only.

## Sources

* `session`: for manage vim session
* `project`: for manage local projects
* `commands`: for manage vim commands
* `location_list`: for manage vim location list
* `quickfix`: for manage vim quickfix list
* `history`: for manage vim history

## Actions

### session

* `load` default action
* `delete` remove selected session

### project

* `open` open denite file_rec of selected project
* `tabopen` open selected project directory in new iTerm2 tab (Mac only)

### commands

* `execute` execute selected command
* `edit` edit selected command

### location_list

Actions of `file` kind

### quickfix

* `cc` run `:cc` command with selected target
* `quickfix` create new quickfix list with selected targets

### history

* `execute` execute selected command/search
* `feedkeys` feedkeys to command line

## LICENSE

Copyright 2017 chemzqm@gmail.com

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
