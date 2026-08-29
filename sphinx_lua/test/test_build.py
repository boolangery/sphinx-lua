"""Content-level regression tests.

A successful ``sphinx-build -W`` only proves nothing raised a warning; it
does not prove the rendered docs are actually correct (e.g. a directive can
silently pick up the wrong id/prefix and still build clean). These tests
assert on the actual generated HTML.
"""


def test_wildcard_automodule_documents_every_matching_module(built_index_html):
    assert 'pl.Second' in built_index_html
    assert 'Create a new Second' in built_index_html


def test_alias_is_rendered_as_lua_alias(built_index_html):
    assert 'id="SourceFn"' in built_index_html
    assert 'class="lua alias"' in built_index_html


def test_param_type_links_to_its_alias_definition(built_index_html):
    assert 'href="#SourceFn"' in built_index_html


def test_custom_type_links_to_its_class_definition(built_index_html):
    assert 'href="#Class"' in built_index_html


def test_markdown_fence_becomes_a_real_code_block(built_index_html):
    assert '```' not in built_index_html
    assert 'highlight-lua' in built_index_html


def test_known_metamethod_uses_metamethod_directive(built_index_html):
    assert 'id="Class.__eq"' in built_index_html
    assert 'class="lua metamethod"' in built_index_html


def test_autofunction_documents_a_global_function(built_index_html):
    # Regression: autofunction previously either crashed (unimplemented) or,
    # once implemented, leaked the preceding automodule's module context
    # into the signature (rendered as "pl.Second.greet" instead of "greet").
    assert 'id="greet"' in built_index_html
    assert 'id="pl.Second.greet"' not in built_index_html
