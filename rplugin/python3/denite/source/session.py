# ============================================================================
# FILE: session.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
import time
from .base import Base
from denite import util
from ..kind.base import Base as BaseKind

def ago(now, seconds):
    diff = now - seconds
    if diff <= 0:
        return 'just now'
    if diff < 60:
        return str(int(diff)) + ' seconds ago'
    if diff/60 < 60:
        return str(int(diff/60)) + ' minutes ago'
    if diff/3.6e+3 < 24:
        return str(int(diff/3.6e+3)) + ' hours ago'
    if diff/8.64e+4 < 24:
        return str(int(diff/8.64e+4)) + ' days ago'
    if diff/6.048e+5 < 4.34812:
        return str(int(diff/6.048e+5)) + ' weeks ago'
    if diff/2.63e+6 < 12:
        return str(int(diff/2.63e+6)) + ' months ago'
    return str(int(diff/3.156e+7)) + 'years ago'

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'session'
        self.kind = Kind(vim)

    def on_init(self, context):
        context['__root'] = self.vim.eval('g:session_directory')

    def highlight(self):
        self.vim.command('highlight default link deniteSessionName Title')
        self.vim.command('highlight default link deniteSessionTime Statement')

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSession /^.*$/ ' +
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSessionName /^\s\?\S\+/ ' +
                         r'contained containedin=deniteSession')
        self.vim.command(r'syntax match deniteSessionTime /(.\{-})/ ' +
                         r'contained containedin=deniteSession')

    def gather_candidates(self, context):
        root = context['__root']
        candidates = []

        items = os.scandir(root)
        now = time.time()
        for item in items:
            if item.is_file():
                mtime = item.stat().st_mtime
                extname = os.path.splitext(item.name)[0]
                candidates.append({
                    'word': '%s (%s)' % (extname, ago(now, mtime)),
                    'action__path': item.path,
                    'source_mtime': mtime
                    })

        candidates = sorted(candidates, key=lambda item: item['source_mtime'],
                            reverse=True)
        return candidates

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.persist_actions += [] #pylint: disable=E1101
        self.redraw_actions += [] #pylint: disable=E1101
        self.default_action = 'load'
        self.name = 'session'

    def action_load(self, context):
        target = context['targets'][0]
        self.vim.call('session#load', target['action__path'])

    def action_delete(self, context):
        for target in context['targets']:
            c = util.input(self.vim, context, 'Delete source %s ?' % (target['action__path']), 'y')
            if c == 'y':
                self.vim.call('delete', target['action__path'])
