# ============================================================================
# FILE: commands.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
import json
from .base import Base
from denite import util
from ..kind.base import Base as BaseKind
from operator import itemgetter

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'commands'
        self.vars = {
            "config": '~/.vim/command.json'
        }

        self.kind = Kind(vim)

    def on_init(self, context):
        context['__config'] = util.expand(self.vars['config'])

    def highlight(self):
        self.vim.command('highlight link uniteSource__CommandSign Type')
        self.vim.command('highlight link uniteSource__CommandTrigger Identifier')
        self.vim.command('highlight link uniteSource__CommandDescription Statement')

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource__CommandHeader /^.*$/ '
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match uniteSource__CommandSign /\v^.{2}/ contained '
                         r'contained containedin=deniteSource__CommandHeader')
        self.vim.command(r'syntax match uniteSource__CommandTrigger /\%6c.*\%18c/ contained '
                         r'contained containedin=deniteSource__CommandHeader')
        self.vim.command(r'syntax match uniteSource__CommandDescription /\%19c.*$/ contained '
                         r'contained containedin=deniteSource__CommandHeader')

    def gather_candidates(self, context):
        if not os.access(context['__config'], os.R_OK):
            return []

        candidates = []
        with open(context['__config']) as fp:
            try:
                config = json.loads(fp.read())
                for obj in config:
                    candidates.append({
                        'word': obj['command'],
                        'abbr': '▷ %-12s %s' % (obj['command'], obj['description']),
                        'source__command': obj['command'],
                        'source__args': obj['args'],
                        'source__config': context['__config'],
                        })
            except json.JSONDecodeError:
                util.error(self.vim, 'Decode error for %s' % context['__config'])

        candidates = sorted(candidates, key=itemgetter('source__command'))
        return candidates

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)
        self.default_action = 'execute'
        self.name = 'commands'
        self.persist_actions = []

    def action_execute(self, context):
        target = context['targets'][0]
        command = target['source__command']
        args = target['source__args']
        if args:
            util.clear_cmdline(self.vim)
            self.vim.call('denite#extra#feedkeys', ':%s' % command)
        else:
            self.vim.call('denite#util#execute_command', command, False)

    def action_edit(self, context):
        target = context['targets'][0]
        command = target['source__command']
        config = target['source__config']
        self.vim.command('silent edit +/"%s %s' % (command, config))
        self.vim.command('normal! zz')
        cursor = self.vim.call('getcurpos')
        cursor[2] = 15
        self.vim.call('setpos', '.', cursor)
