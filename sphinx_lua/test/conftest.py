from pathlib import Path

import pytest
from sphinx.application import Sphinx

TEST_DIR = Path(__file__).parent


@pytest.fixture(scope='session')
def built_index_html(tmp_path_factory):
    """Build the test Sphinx project once (warnings-as-errors, like CI) and
    return the rendered index.html, so tests can assert on actual output
    rather than just "did the build succeed".

    Deliberately does not chdir into confdir first: lua_source_path is
    resolved relative to confdir, not the process cwd, and pytest's cwd is
    normally the repo root.

    """
    outdir = tmp_path_factory.mktemp('sphinx-lua-build')
    app = Sphinx(
        srcdir=str(TEST_DIR),
        confdir=str(TEST_DIR),
        outdir=str(outdir),
        doctreedir=str(outdir / '.doctrees'),
        buildername='html',
        warningiserror=True,
    )
    app.build()
    return (outdir / 'index.html').read_text(encoding='utf8')
