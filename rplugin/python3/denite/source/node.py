# ============================================================================
# FILE: node.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
import json
import re
import shlex
import subprocess
from .base import Base
from denite import util
from ..kind.base import Base as BaseKind
from operator import itemgetter

BROWSER_MAP = {
    'dom': 'dom-easy',
    'cookie': 'component-cookie',
    'menu': 'component-menu',
    'ago': 'component-ago',
    'align': 'component-align',
    'drop': 'component-drop',
    'dropdown': 'component-dropdown',
    'file-picker': 'component-file-picker',
    'upload': 'component-upload',
    'request': 'request-component',
    'spin': 'component-spin',
    'spinner': 'component-spinner',
    'notice': 'component-notice',
    'overlay': 'overlay-component',
    'uid': 'component-uid',
    'query': 'component-query',
    'querystring': 'component-querystring',
    'delegate': 'component-delegate',
    'classes': 'component-classes',
    'closest': 'component-closest',
    'emitter': 'component-emitter',
    'events': 'component-events',
    'event': 'component-event',
    'indexof': 'component-indexof',
    'sortable': 'sortable-component',
    'matches-selector': 'component-matches-selector',
    'radio': 'radio-component',
    'switch': 'switch-component',
    'validate': 'validate-component',
    'invalid': 'invalid-component',
    'delay': 'delay-component',
    'reduce': 'reduce-component',
    'model': 'model-component',
    'reactive': 'reactive-lite',
    'iscroll': 'iscroll-component',
    'scrollfix': 'component-scrollfix',
    'tap-event': 'component-tap-event',
    'traverse': 'yields-traverse',
    'tween': 'component-tween',
    'tap': 'component-tap',
    'more': 'more-mobile',
    'pager': 'component-pager',
    'raf': 'component-raf',
    'tab': 'tab-component',
    'style': 'style-component'
}

def _find_json(path):
    while True:
        if path == '/' or os.path.ismount(path):
            return None
        p = os.path.join(path, 'package.json')
        if os.access(p, os.R_OK):
            return p
        path = os.path.dirname(path)

def run_command(commands, cwd):
    try:
        p = subprocess.run(commands,
                           cwd=cwd,
                           encoding="utf8",
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return []
    return p.stdout.split('\n')

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'node'
        self.kind = Kind(vim)

    def on_init(self, context):
        cwd = os.path.normpath(self.vim.call('getcwd'))
        context['__package'] = _find_json(cwd)

    def highlight(self):
        self.vim.command('highlight default link deniteNodeName Title')
        self.vim.command('highlight default link deniteNodeVersion Statement')
        self.vim.command('highlight default link deniteNodeDev Comment')

    def define_syntax(self):
        self.vim.command(r'syntax match deniteNode /^.*$/ ' +
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteNodeName /^\s\?\S\+/ ' +
                         r'contained containedin=deniteNode')
        self.vim.command(r'syntax match deniteNodeVersion /(.\{-})/ ' +
                         r'contained containedin=deniteNode')
        self.vim.command(r'syntax match deniteNodeDev /\v\[D\]/ ' +
                         r'contained containedin=deniteNode')

    def gather_candidates(self, context):
        package = context['__package']
        if not package:
            util.error(self.vim, 'package.json not found')
            return []

        root = os.path.dirname(package)
        items = []
        with open(package) as fp:
            try:
                obj = json.loads(fp.read())
                browser = {v: k for k, v in obj.get('browser', {}).items()}
                deps = obj.get('dependencies')
                devDeps = obj.get('devDependencies')
                if deps:
                    items += [{'name': x, 'dev': False, 'alias': browser.get(x, '')}
                              for x in deps]
                if devDeps:
                    items += [{'name': x, 'dev': True, 'alias': browser.get(x, '')}
                              for x in devDeps]
            except json.JSONDecodeError:
                util.error(self.vim, 'Decode error for %s' % package)
                return []

        candidates = []
        for item in items:
            jsonpath = os.path.join(root, 'node_modules', item['name'], 'package.json')
            if not os.access(jsonpath, os.R_OK):
                continue
            stat = os.stat(jsonpath)
            with open(jsonpath) as fp:
                try:
                    obj = json.loads(fp.read())
                    mtime = stat.st_mtime
                    version = obj.get('version', 'unknown')
                    name = item['alias'] if item['alias'] else item['name']
                    candidates.append({
                        'word': item['name'],
                        'abbr': '%s (%s) %s' % (name, version, '[D]' if item['dev'] else ''),
                        'action__path': os.path.dirname(jsonpath),
                        'source__prod': not item['dev'],
                        'source__mtime': mtime,
                        'source__root': root,
                        'source__name': item['name'],
                        })
                except json.JSONDecodeError:
                    util.error(self.vim, 'Decode error for %s' % jsonpath)
                    continue

        candidates = sorted(candidates, key=itemgetter('source__prod', 'source__mtime'),
                            reverse=True)
        return candidates

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.persist_actions += ['delete'] #pylint: disable=E1101
        self.redraw_actions += ['delete'] #pylint: disable=E1101
        self.default_action = 'open'
        self.name = 'node'
        self.isWin = self.vim.call('has', 'win32') or self.vim.call('has', 'win64')
        self.isMac = self.vim.call('has', 'mac')

    def action_open(self, context):
        target = context['targets'][0]
        self.vim.command('Denite file_rec:%s' % target['action__path'])

    def action_tabopen(self, context):
        target = context['targets'][0]
        if not self.isMac:
            util.error(self.vim, context, 'Tabopen only supported on Mac')
            return
        self.vim.call('denite#extra#iterm_tabopen', target['action__path'])

    def action_update(self, context):
        target = context['targets'][0]
        dev = '' if target['source__prod'] else '-dev'
        cmd = 'npm install %s@latest --save%s' % (target['source__name'], dev)
        self.vim.call('denite#node#update',
                      cmd, target['action__path'], target['source__root'])

    def action_preview(self, context):
        target = context['targets'][0]
        jsonpath = os.path.join(target['action__path'], 'package.json')
        self.vim.command('split %s' % jsonpath)

    def action_browser(self, context):
        target = context['targets'][0]
        url = 'https://www.npmjs.com/package/%s' % target['source__name']
        self.vim.call('denite#util#open', url)

    def action_help(self, context):
        target = context['targets'][0]
        items = os.scandir(target['action__path'])
        pattern = re.compile(r'readme\.md', re.I) #pylint: disable=E1101
        for item in items:
            if item.is_file() and pattern.match(item.name):
                self.vim.command('split %s' % item.path)
                break

    def action_find(self, context):
        target = context['targets'][0]
        name = target['source__name']
        self.vim.command('Denite func:m:%s' % name)

    def action_delete(self, context):
        for target in context['targets']:
            c = util.input(self.vim, context, 'Delete module %s ?' % target['source__name'], 'y')
            contains = '"%s":' % target['source__name']
            if c == 'y':
                if self.isWin:
                    self.vim.call('delete', target['action__path'], 'rf')
                else:
                    if self.vim.call('executable', 'rmtrash'):
                        cmd = 'rmtrash %s' % target['action__path']
                    else:
                        cmd = 'rm -rf %s' % target['action__path']
                    self.vim.call('system', cmd)
                    if self.vim.eval('v:shell_error') == 0:
                        jsonpath = os.path.join(target['source__root'], 'package.json')
                        with open(jsonpath, "r") as fp:
                            lines = fp.readlines()
                            f = open(jsonpath, "w")
                            for line in lines:
                                if contains not in line:
                                    f.write(line)
                            f.close()

    def action_add(self, context):
        s = util.input(self.vim, context, 'Install: ')
        args = shlex.split(s)
        newArgs = []
        target = context['targets'][0]
        jsonpath = os.path.join(target['source__root'], 'package.json')
        with open(jsonpath, 'r') as fp:
            obj = json.loads(fp.read())
            if not 'browser' in obj:
                obj['browser'] = {}
            for arg in args:
                if arg in BROWSER_MAP:
                    newArgs.append(BROWSER_MAP[arg])
                    obj['browser'][arg] = BROWSER_MAP[arg]
                else:
                    newArgs.append(arg)
            f = open(jsonpath, 'w')
            f.write(json.dumps(obj, indent=2))
            f.close()

        opt = next(filter(lambda x: x[0] == '-', newArgs), None)
        if not opt:
            newArgs.append('-S')
        self.vim.call('denite#node#install', newArgs, target['source__root'])
