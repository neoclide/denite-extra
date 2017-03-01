# ============================================================================
# FILE: history.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
import re
from .base import Base
from denite import util
from ..kind.base import Base as BaseKind
from operator import itemgetter

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'history'
        self.kind = Kind(vim)


    def gather_candidates(self, context):
        args = dict(enumerate(context['args']))
        t = args.get(0, 'cmd')
        pattern = re.compile(r'\s*(\d+|#)\s+(.+)')

        res = self.vim.call('execute', 'history %s' % t)
        candidates = []
        for line in res.split("\n"):
            if not line:
                continue
            m = pattern.match(line)
            if not m:
                continue
            candidates.append({
                'word': '%s %s' % (m.group(1), m.group(2)),
                'source__nr': m.group(1),
                'source__type': t,
                'source__word': m.group(2),
                })

        candidates = sorted(candidates, key=itemgetter('source__nr'))
        return candidates

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)
        self.default_action = 'execute'
        self.name = 'history'
        self.persist_actions = ['delete']
        self.redraw_actions = ['delete']

    def action_execute(self, context):
        target = context['targets'][0]
        command = target['source__word']
        util.clear_cmdline(self.vim)
        self.vim.call('denite#util#feedkeys', command)

    def action_delete(self, context):
        for target in context['targets']:
            nr = int(target['source__nr']) if target['source__nr'] != '#' else '#'
            self.vim.call('histdel', target['source__type'], nr)
