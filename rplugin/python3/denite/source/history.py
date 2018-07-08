# ============================================================================
# FILE: history.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import re
from .base import Base
from denite import util
from ..kind.command import Kind as CommandKind
from operator import itemgetter

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'history'
        self.kind = Kind(vim)


    def gather_candidates(self, context):
        context['is_interactive'] = True
        args = dict(enumerate(context['args']))
        t = args.get(0, 'all')
        pattern = re.compile(r'>?\s*(\d+)\s+(.+)')
        type_pattern = re.compile(r'\s*#\s+(.+)\shistory')

        res = self.vim.call('execute', 'history %s' % t)
        htype = ''

        candidates = []
        for line in res.split("\n"):
            if not line:
                continue
            ms = type_pattern.match(line)
            if ms:
                htype = ms.group(1)
                continue
            else:
                m = pattern.match(line)
                if not m:
                    continue

            pre = ':' if htype == 'cmd' else '/'
            candidates.append({
                'word': '%s%s' % (pre, m.group(2)),
                'action__is_pause': True,
                'source__nr': int(m.group(1)),
                'source__type': htype,
                'source__word': m.group(2),
                })

        candidates = sorted(candidates, key=itemgetter('source__nr'), reverse=True)
        return candidates

class Kind(CommandKind):
    def __init__(self, vim):
        super().__init__(vim)
        self.default_action = 'execute'
        self.name = 'history'
        self.persist_actions = ['delete']
        self.redraw_actions = ['delete']

    def action_feedkeys(self, context):
        target = context['targets'][0]
        command = target['source__word']
        util.clear_cmdline(self.vim)
        if target['source__type'] == 'search':
            keys = '/%s' % command
        elif target['source__type'] == 'cmd':
            keys = ':%s' % command
        else:
            keys = command
        self.vim.call('denite#extra#feedkeys', keys)

    def action_execute(self, context):
        target = context['targets'][0]
        command = target['source__word']
        util.clear_cmdline(self.vim)
        if target['source__type'] == 'search':
            self.vim.call('denite#extra#search', command)
        else:
            self._execute(context,
                command,
                target.get('action__is_pause', False))



    def action_delete(self, context):
        for target in context['targets']:
            nr = int(target['source__nr'])
            self.vim.call('histdel', target['source__type'], nr)
