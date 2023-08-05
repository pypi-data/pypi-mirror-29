from ..command import run_command
from ..util import merge_dicts
from .base import BaseProvider

import os
import os.path
import shutil



class CompileProvider(BaseProvider):
    '''
    Compiles static files, such as *.scss or *.less, when an output file
    timestamp is older than the source file. In production mode, this check
    is done only once (the first time a template is run) per server start.

    Special format keywords for use in the options:
        {appname} - The app name for the template being rendered.
        {template} - The name of the template being rendered, without its extension.
        {appdir} - The app directory for the template being rendered (full path).
        {staticdir} - The static directory as defined in settings.
    '''
    # the command line should be specified as a list (see the subprocess module)
    default_options = merge_dicts(BaseProvider.default_options, {
        'group': 'styles',
        'source': '{appdir}/somedir/{template}.source',
        'output': '{appdir}/somedir/{template}.output',
        'command': [ 'echo', '{appdir}/somedir/{template}.source', '{appdir}/somedir/{template}.output' ],
    })
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        source_path = self.options_format(self.options['source'])
        if os.path.exists(source_path):
            source_stat = os.stat(source_path)
            compiled_path = self.options_format(self.options['output'])
            compiled_exists = os.path.exists(compiled_path)
            compiled_stat = os.stat(compiled_path) if compiled_exists else None
            if not compiled_exists or source_stat.st_mtime > compiled_stat.st_mtime:
                run_command(*[ self.options_format(a) for a in self.options['command'] ])


class CompileScssProvider(CompileProvider):
    '''Specialized CompileProvider that contains settings for *.scss files.'''
    default_options = merge_dicts(CompileProvider.default_options, {
        'source': '{appdir}/styles/{template}.scss',
        'output': '{appdir}/styles/{template}.css',
        'command': [ shutil.which('scss'), '--load-path=.', '--unix-newlines', '{appdir}/styles/{template}.scss', '{appdir}/styles/{template}.css' ],
    })


class CompileLessProvider(CompileProvider):
    '''Specialized CompileProvider that contains settings for *.less files.'''
    default_options = merge_dicts(CompileProvider.default_options, {
        'source': '{appdir}/styles/{template}.less',
        'output': '{appdir}/styles/{template}.css',
        'command': [ shutil.which('lessc'), '--source-map', '{appdir}/styles/{template}.less', '{appdir}/styles/{template}.css' ],
    })

