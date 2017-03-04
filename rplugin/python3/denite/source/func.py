# ============================================================================
# FILE: func.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
import subprocess
from denite import util
from .base import Base

def _find_root(path):
    while True:
        if path == '/' or os.path.ismount(path):
            return None
        p = os.path.join(path, 'package.json')
        if os.access(p, os.R_OK):
            return path
        path = os.path.dirname(path)

def run_command(commands, cwd, stdin=None):
    try:
        p = subprocess.run(commands,
                           cwd=cwd,
                           input=stdin,
                           encoding="utf8",
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return []
    return p.stdout.split('\n')

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'func'
        self.kind = 'file'

    def on_init(self, context):
        cwd = os.path.normpath(self.vim.call('getcwd'))
        context['__root'] = _find_root(cwd)

    def highlight(self):
        self.vim.command('highlight default link deniteSource_funcFile Comment')
        self.vim.command('highlight default link deniteSource_funcLinenr LineNR')

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource_funcHeader /^.*$/ '
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource_funcFile /[^:]*: / '
                         r'contained containedin=deniteSource_funcHeader')
        self.vim.command(r'syntax match deniteSource_funcLinenr /\s*\d\+: / '
                         r'contained containedin=deniteSource_funcHeader')
        self.vim.command(r'syntax match deniteSource_funcSeparator /:/ conceal '
                         r'contained containedin=deniteSource_funcHeader')

    def gather_candidates(self, context):
        if not context['__root']:
            util.error(self.vim, 'package.json not found')
            return []
        root = context['__root']
        args = dict(enumerate(context['args']))
        t = args.get(0, '')
        cmds = ['parsefunc']
        curpath = os.path.normpath(self.vim.call('expand', '%:p'))
        relpath = os.path.relpath(curpath, root)
        if t == 't':
            cmds += ['-m', 'this']
        elif t == 'm':
            name = args.get(1, '')
            if name:
                cmds += ['-m', name]
            else:
                cmds += ['-a']
        elif t == 'r':
            cmds += ['-r', relpath]
        elif t == 'e':
            cmds += ['-m', relpath]
        else:
            cmds += [relpath]

        candidates = []
        if not len(t):
            stdin = "\n".join(self.vim.call('getline', 1, '$'))
            lines = run_command(cmds, root, stdin)
        else:
            lines = run_command(cmds, root)
        for line in lines:
            if not line:
                continue
            parts = line.split(':')
            filepath = relpath if parts[0] == 'stdin' else parts[0]
            if parts[0] == 'stdin':
                actionpath = curpath
                abbr = os.path.basename(curpath)
            elif os.path.isabs(parts[0]):
                actionpath = parts[0]
                abbr = os.path.relpath(filepath, os.path.join(root, 'node_modules'))
            else:
                actionpath = os.path.join(root, parts[0])
                abbr = os.path.relpath(actionpath, root)
            candidates.append({
                'word': parts[2],
                'abbr': '%s: %s: %s' % (abbr, parts[1], parts[2]),
                'action__path': actionpath,
                'action__line': parts[1],
                })
        return candidates
