import os
from sphinx.util import logging
from luadoc.core import FilesProcessor, DocOptions

logger = logging.getLogger(__name__)


def run_luadoc(app):
    """Run LUADoc across a whole codebase, and squirrel away its results."""

    modules = []
    for source_dir in app.config.lua_source_path:
        logger.debug('building lua documentation model for source dir: ' + source_dir)

        filenames = []
        # build a filename list
        if not os.path.isdir(source_dir):
            filenames.append(source_dir)
        else:
            for root, subdirs, files in os.walk(source_dir):
                for filename in files:
                    if filename.endswith('lua'):
                        filepath = os.path.join(root, filename)
                        filenames.append(filepath)

        options = DocOptions()
        options.encoding = app.config.lua_source_encoding
        options.comment_prefix = app.config.lua_source_comment_prefix
        options.emmy_lua_syntax = app.config.lua_source_use_emmy_lua_syntax
        options.private_prefix = app.config.lua_source_private_prefix

        # build model for files
        model = FilesProcessor(8, options).run(filenames)
        modules.extend(model)

    app._sphinxlua_modules = modules
