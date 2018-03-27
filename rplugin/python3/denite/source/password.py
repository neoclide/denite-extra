# ============================================================================
# FILE: apssword.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
from .base import Base
from ..kind.base import Base as BaseKind

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'pass'
        self.kind = Kind(vim)

    def gather_candidates(self, context):
        candidates = []

        items = self.vim.call('password#list')
        root = self.vim.call('getcwd')

        for item in items:
            candidates.append({
                'word': item,
                'source__root': root
                })
        return candidates

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.default_action = 'show'
        self.name = 'pass'

    def action_show(self, context):
        target = context['targets'][0]
        self.vim.call('denite#extra#iterm_tabrun', target['source__root'],
                      'pass show ' + target['word'])
