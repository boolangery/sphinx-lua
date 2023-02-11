from .directives import (auto_class_directive_bound_to_app,
                         auto_function_directive_bound_to_app,
                         auto_module_directive_bound_to_app,
                         auto_class_summary_directive_bound_to_app)
from .luadoc import run_luadoc


def setup(app):
    # I believe this is the best place to run luadoc. I was tempted to use
    # app.add_source_parser(), but I think the kind of source it's referring to
    # is RSTs.
    app.connect('builder-inited', run_luadoc)

    app.connect('env-before-read-docs', read_all_docs)

    app.add_directive_to_domain('lua',
                                'autofunction',
                                auto_function_directive_bound_to_app(app))
    app.add_directive_to_domain('lua',
                                'autoclass',
                                auto_class_directive_bound_to_app(app))
    app.add_directive_to_domain('lua',
                                'automodule',
                                auto_module_directive_bound_to_app(app))
    app.add_directive_to_domain('lua',
                                'autoclasssummary',
                                auto_class_summary_directive_bound_to_app(app))
    # TODO: We could add a lua:module with app.add_directive_to_domain().

    app.add_config_value('lua_source_path', ['./'], 'env')
    app.add_config_value('lua_source_encoding', 'utf8', 'env')
    app.add_config_value('lua_source_comment_prefix', '---', 'env')
    app.add_config_value('lua_source_use_emmy_lua_syntax', True, 'env')
    app.add_config_value('lua_source_private_prefix', '_', 'env')
    app.add_config_value('luadoc_config_path', None, 'env')


def read_all_docs(app, env, doc_names):
    """Add all found docs to the to-be-read list, because we have no way of
    telling which ones reference LUA code that might have changed.

    Otherwise, builds go stale until you touch the stale RSTs or do a ``make
    clean``.

    """
    doc_names[:] = env.found_docs
