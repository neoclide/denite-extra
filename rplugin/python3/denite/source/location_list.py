# ============================================================================
# FILE: location_list.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
from .base import Base

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'location_list'
        self.kind = 'file'
        self.matchers = ['matcher_regexp']
        self.sorters = []

    def on_init(self, context):
        context['__linenr'] = self.vim.current.window.cursor[0]
        context['__bufname'] = self.vim.current.buffer.name
        context['__bufnr'] = self.vim.current.buffer.number
        context['__filename'] = os.path.basename(context['__bufname'])

    def define_syntax(self):
        self.vim.command('syntax case ignore')
        self.vim.command(r'syntax match deniteSource__LocationListHeader '
                         r'/\v^.*\|\d.{-}\|/ containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource__LocationListName '
                         r'/\v^[^|]+/ contained containedin=deniteSource__LocationListHeader')
        self.vim.command(r'syntax match deniteSource__LocationListPosition '
                         r'/\v\|\zs.{-}\ze\|/ contained containedin=deniteSource__LocationListHeader')
        self.vim.command(r'syntax match deniteSource__LocationListError /\vError/ contained containedin=deniteSource__LocationListPosition')
        self.vim.command(r'syntax match deniteSource__LocationListWarning /\vWarning/ contained containedin=deniteSource__LocationListPosition')

    def highlight(self):
        self.vim.command('highlight default link deniteSource__LocationListWarning Comment')
        self.vim.command('highlight default link deniteSource__LocationListError Error')
        self.vim.command('highlight default link deniteSource__LocationListName Identifier')
        self.vim.command('highlight default link deniteSource__LocationListPosition LineNr')

    def convert(self, val, context):
        type_str = 'Error' if val['type'].lower() == 'e' else 'Warning'
        bufnr = val['bufnr']
        line = val['lnum'] if bufnr != 0 else 0
        col = val['col'] if bufnr != 0 else 0

        if len(context['__bufname']) == 0:
            word = val['text']
        else:
            word = context['__filename'] + ' |' + str(line) + ' col ' + str(col) + ' ' + type_str + '| ' + val['text']

        return {
            'word': word.replace('\n', ' '),
            'action__path': context['__bufname'],
            'action__line': line,
            'action__col': col,
            'action__buffer_nr': context['__bufnr']
            }

    def gather_candidates(self, context):
        winnr = self.vim.eval('bufwinnr("' + context['__bufname'] + '")')
        items = self.vim.eval('getloclist(' + str(winnr) + ')')
        res = []
        for item in items:
            if item['valid'] != 0:
                res.append(self.convert(item, context))
        return res
