# ============================================================================
# FILE: quickfix.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import re
from .base import Base

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'quickfix'
        self.kind = 'file'
        self.matchers = ['matcher_fuzzy']
        self.sorters = []

    def define_syntax(self):
        self.vim.command('syntax case ignore')
        self.vim.command(r'syntax match deniteSource_QuickfixHeader /\v^.*$/ containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource_QuickfixName /\v^[^|]+/ contained '
                r'containedin=deniteSource_QuickfixHeader')
        self.vim.command(r'syntax match deniteSource_QuickfixPosition /\v\|\zs.{-}\ze\|/ contained '
                r'containedin=deniteSource_QuickfixHeader')
        word = self.vim.eval('get(g:,"grep_word", "")')
        if word:
            pattern = re.escape(word)
            self.vim.command(r'syntax match deniteSource_QuickfixWord /%s/' % pattern)

    def highlight(self):
        self.vim.command('highlight default link deniteSource_QuickfixWord Search')
        self.vim.command('highlight default link deniteSource_QuickfixName Directory')
        self.vim.command('highlight default link deniteSource_QuickfixPosition LineNr')


    def convert(self, val, context):
        bufnr = val['bufnr']
        line = val['lnum'] if bufnr != 0 else 0
        col = val['col'] if bufnr != 0 else 0
        fname = "" if bufnr == 0 else self.vim.eval('bufname(' + str(bufnr) + ')')
        word = '{fname} |{location}| {text}'.format(
            fname=fname,
            location='' if line == 0 and col == 0 else '%d col %d' % (line, col),
            text=val['text'])

        return {
            'word': word,
            'action__path': fname,
            'action__line': line,
            'action__col': col,
            'action__buffer_nr': bufnr,
            }

    def gather_candidates(self, context):
        items = self.vim.eval('getqflist()')
        res = []

        for item in items:
            if item['valid'] != 0:
                res.append(self.convert(item, context))
        return res
