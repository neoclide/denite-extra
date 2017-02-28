# Denite-extra

Some extra sources for [denite.nvim](https://github.com/Shougo/denite.nvim).

## Sources

* `session`: for manage vim session
* `node`: for manage node modules
* `project`: for manage local projects
* `command`: for manage vim commands

## Actions

### session

* `load` default action
* `delete` remove selected session

### node

* `open` open denite file_rec of selected module
* `tabopen` open selected module directory in new iTerm2 tab
* `help` open Readme.md file of selected module
* `preview` open package.json in preview window
* `browser` open module in default browser
* `update` update selected module(s) to latest version
* `delete` delete module directory and field from package.json

### project

* `open` open denite file_rec of selected project
* `tabopen` open selected project directory in new iTerm2 tab

### command

* `execute` execute selected command
* `edit` edit selected command

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
