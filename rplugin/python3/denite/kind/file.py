from denite.kind.file import Kind as DefaultKind


class Kind(DefaultKind):

    def action_quickfix(self, context):
        """ Use the default file 'kind', but override quickfix, so that it uses
        'Denite quickfix' rather than 'copen'
        """

        qflist = [{
            'filename': x['action__path'],
            'lnum': x['action__line'],
            'text': x['action__text'],
        } for x in context['targets']
                  if 'action__line' in x and 'action__text' in x]
        self.vim.call('setqflist', qflist)
        # TODO this appears to only partially work - perhaps there is a better
        # way to refresh denite
        self.vim.command('Denite quickfix -auto-resize -mode=normal')
