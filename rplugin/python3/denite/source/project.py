# ============================================================================
# FILE: project.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
from .base import Base
from denite import util
from ..kind.base import Base as BaseKind
from operator import itemgetter
from os.path import normpath

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'project'
        self.kind = Kind(vim)
        self.sorters = []

    def on_init(self, context):
        folders = self.vim.vars.get('project_folders', [])
        context['__folders'] = [util.expand(normpath(x)) for x in folders]

    def highlight(self):
        self.vim.command('highlight link deniteSource__ProjectRoot Comment')
        self.vim.command('highlight link deniteSource__ProjectName Identifier')

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource__ProjectHeader /^.*$/ '
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource__ProjectRoot /^.*\%16c/ contained '
                         r'contained containedin=deniteSource__ProjectHeader')
        self.vim.command(r'syntax match deniteSource__ProjectName /\%17c.*$/ contained '
                         r'contained containedin=deniteSource__ProjectHeader')

    def gather_candidates(self, context):
        candidates = []
        for directory in context['__folders']:
            if not os.access(directory, os.X_OK):
                continue
            base = os.path.basename(directory)
            items = os.scandir(directory)
            for item in items:
                if item.name[0] == '.':
                    continue
                candidates.append({
                    'word': item.name,
                    'abbr': '%-14s %-20s' % (base, item.name),
                    'source__root': item.path,
                    'source__mtime': item.stat().st_mtime
                    })
        candidates = sorted(candidates, key=itemgetter('source__mtime'),
                            reverse=True)
        return candidates

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.default_action = 'open'
        self.name = 'project'

    def action_open(self, context):
        target = context['targets'][0]
        self.vim.command('Denite file_rec:%s' % target['source__root'])

    def action_tabopen(self, context):
        target = context['targets'][0]
        self.vim.call('denite#extra#iterm_tabopen', target['source__root'])
