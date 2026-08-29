from collections import OrderedDict
from json import dumps
import re
import os

from docutils.parsers.rst import Parser as RstParser
from docutils.statemachine import StringList
from docutils.utils import new_document
from jinja2 import Environment, PackageLoader
from six import iteritems, string_types
from sphinx.errors import SphinxError
from sphinx.util import rst

from sphinx.util import logging

logger = logging.getLogger(__name__)


class LuaRenderer(object):
    """Abstract superclass for renderers of various sphinx-lua directives

    Provides an inversion-of-control framework for rendering and bridges us
    from the hidden, closed-over LuaDirective subclasses to top-level classes
    that can see and use each other. Handles parsing of a single, all-consuming
    argument that consists of a LUA entity reference and an optional formal
    parameter list.

    """

    def __init__(self, directive, app, arguments=None, content=None, options=None):
        # Fix crash when calling eval_rst with CommonMarkParser:
        if not hasattr(directive.state.document.settings, 'tab_width'):
            directive.state.document.settings.tab_width = 8

        self._directive = directive

        # content, arguments, options, app: all need to be accessible to
        # template_vars, so we bring them in on construction and stow them away
        # on the instance so calls to template_vars don't need to concern
        # themselves with what it needs.
        self._app = app
        self._partial_path = arguments[0]
        self._content = content or StringList()
        self._options = options or {}

    @classmethod
    def from_directive(cls, directive, app):
        """Return one of these whose state is all derived from a directive.

        This is suitable for top-level calls but not for when a renderer is
        being called from a different renderer, lest content and such from the
        outer directive be duplicated in the inner directive.

        :arg directive: The associated Sphinx directive
        :arg app: The Sphinx global app object. Some methods need this.

        """
        return cls(directive,
                   app,
                   arguments=directive.arguments,
                   content=directive.content,
                   options=directive.options)

    def rst_nodes(self):
        """Render into RST nodes a thing shaped like a function, having a name
        and arguments.

        Fill in args, docstrings, and info fields from stored LUADoc output.

        """
        raise NotImplementedError()

    def rst(self, args_dict):
        """Return rendered RST about an entity with the given name and doclet."""

        def process_link(s):
            """A non-optimal implementation of a regex filter"""
            return re.sub(r'@{\s*([\w.]*)\s*}', r':lua:class:`\1`', s)

        def render_code_fences(s):
            """Turn Markdown fenced code blocks (```lang\\ncode\\n```), as
            commonly found in EmmyLua doc comments, into RST code-block
            directives so they render instead of showing up as literal text.

            """
            def repl(match):
                language = match.group(1) or 'lua'
                code = match.group(2)
                indented = '\n'.join('    ' + line if line.strip() else ''
                                     for line in code.splitlines())
                return '\n\n.. code-block:: %s\n\n%s\n\n' % (language, indented)

            return re.sub(r'```(\w*)\n(.*?)```', repl, s, flags=re.DOTALL)

        def link_custom_type(name):
            """Turn a custom type name into a cross-reference if it matches a
            known class or alias, so params/returns using ``@alias``-defined
            types link to their definition. Falls back to plain text for
            unknown names to avoid emitting dangling cross-references.

            """
            for module in getattr(self._app, '_sphinxlua_modules', []):
                for alias in getattr(module, 'aliases', []):
                    if alias.name == name:
                        return ':lua:alias:`%s`' % name
                for cls in module.classes:
                    if cls.name == name:
                        return ':lua:class:`%s`' % name
            return name

        def start_stop_line(doc_node, file_path):
            """ Return start stop line in the form '1-5' """
            file_path = os.path.join(self._app.confdir, file_path)
            with open(file_path, "r") as f:
                content = f.read()
            total_lines = content.count('\n') + 1
            start_line = content[:doc_node.start_char].count('\n') + 1
            stop_line = content[:doc_node.stop_char].count('\n') + 1
            # Clamp to actual file line count (avoid "out of range" with Sphinx -W)
            stop_line = min(stop_line, total_lines)
            return str(start_line) + "-" + str(stop_line)

        # Render to RST using Jinja:
        env = Environment(loader=PackageLoader('sphinx_lua', 'templates'))
        env.filters['process_link'] = process_link
        env.filters['link_custom_type'] = link_custom_type
        env.filters['render_code_fences'] = render_code_fences
        env.filters['start_stop_line'] = start_stop_line
        template = env.get_template(self._template)
        return template.render(**args_dict)

    def _name(self):
        """Return the LUA function or class longname."""
        return self._arguments[0].split('(')[0]

    def _fields(self, doclet):
        """Return an iterable of "info fields" to be included in the directive,
        like params, return values, and exceptions.

        Each field consists of a tuple ``(heads, tail)``, where heads are
        words that go between colons (as in ``:param string href:``) and
        tail comes after.

        """
        FIELD_TYPES = OrderedDict([('params', _params_formatter),
                                   ('properties', _params_formatter),
                                   ('exceptions', _exceptions_formatter),
                                   ('returns', _returns_formatter)])
        for field_name, callback in iteritems(FIELD_TYPES):
            for field in doclet.get(field_name, []):
                description = field.get('description', '')
                unwrapped = re.sub(r'[ \t]*[\r\n]+[ \t]*', ' ', description)
                yield callback(field, unwrapped)


class AutoFunctionRenderer(LuaRenderer):
    _template = 'function.rst'

    def rst_nodes(self):
        """Render a global (non-method, non-static) LUA function."""
        lua_function = None

        for module in self._app._sphinxlua_modules:
            for func in module.functions:
                if func.name == self._partial_path:
                    lua_function = func
                    break

        if not lua_function:
            raise SphinxError('No LUADoc documentation was found for object "%s" or any path ending with that.'
                              % self._partial_path)

        rst = self.rst(dict(function=lua_function))
        doc = new_document('%s' % self._partial_path, settings=self._directive.state.document.settings)

        RstParser().parse(rst, doc)
        return doc.children


class AutoClassRenderer(LuaRenderer):
    _template = 'class.rst'

    def rst_nodes(self):
        """Render into RST nodes a thing shaped like a function, having a name
        and arguments.

        Fill in args, docstrings, and info fields from stored LUADoc output.

        """
        lua_class = None
        module = None

        # lookup for class
        for mod in self._app._sphinxlua_modules:
            for cls in mod.classes:
                if cls.name == self._partial_path:
                    lua_class = cls
                    module = mod
                    break

        if not lua_class:
            raise SphinxError('No LUADoc documentation was found for object "%s" or any path ending with that.'
                              % self._partial_path)

        rst = self.rst(dict(
            name=self._partial_path,
            model=lua_class,
            file_path=os.path.relpath(module.file_path, self._app.confdir),
            options=self._options
        ))
        doc = new_document('%s' % self._partial_path, settings=self._directive.state.document.settings)

        RstParser().parse(rst, doc)
        return doc.children


class AutoAliasRenderer(LuaRenderer):
    _template = 'alias.rst'

    def rst_nodes(self):
        """Render an ``@alias``-declared type as a ``lua:alias`` directive."""
        lua_alias = None

        for module in self._app._sphinxlua_modules:
            for alias in getattr(module, 'aliases', []):
                if alias.name == self._partial_path:
                    lua_alias = alias
                    break

        if not lua_alias:
            raise SphinxError('No LUADoc documentation was found for object "%s" or any path ending with that.'
                              % self._partial_path)

        rst = self.rst(dict(model=lua_alias))
        doc = new_document('%s' % self._partial_path, settings=self._directive.state.document.settings)

        RstParser().parse(rst, doc)
        return doc.children


class AutoModuleRenderer(LuaRenderer):
    _template = 'module.rst'

    def rst_nodes(self):
        """Render into RST nodes a thing shaped like a function, having a name
        and arguments.

        Fill in args, docstrings, and info fields from stored LUADoc output.

        An exact module name is looked up first. If none matches, the argument
        is treated as a regex pattern and every module whose name matches it is
        rendered, allowing e.g. ``.. lua:automodule:: .*`` to document every
        module found in ``lua_source_path`` in one shot.

        """
        all_modules = self._app._sphinxlua_modules

        lua_modules = [m for m in all_modules if m.name == self._partial_path]

        if not lua_modules:
            pattern = re.compile(self._partial_path)
            lua_modules = [m for m in all_modules if pattern.match(m.name)]

        if not lua_modules:
            raise SphinxError('No LUADoc documentation was found for object "%s" or any path ending with that.'
                              % self._partial_path)

        rst = '\n\n'.join(
            self.rst(dict(name=lua_module.name, module=lua_module))
            for lua_module in sorted(lua_modules, key=lambda m: m.name))

        doc = new_document('%s' % self._partial_path, settings=self._directive.state.document.settings)
        RstParser().parse(rst, doc)
        return doc.children


class AutoClassSummaryRenderer(LuaRenderer):
    _template = 'classsummary.rst'

    def rst_nodes(self):
        """Render into RST nodes a thing shaped like a function, having a name
        and arguments.

        Fill in args, docstrings, and info fields from stored LUADoc output.

        """
        pattern = self._partial_path

        lua_classes = []

        # lookup for class
        for module in self._app._sphinxlua_modules:
            for cls in module.classes:
                if re.match(pattern, cls.name):
                    lua_classes.append(cls)

        rst = self.rst(dict(
            name=self._partial_path,
            model=lua_classes,
        ))

        doc = new_document('%s' % self._partial_path, settings=self._directive.state.document.settings)

        RstParser().parse(rst, doc)
        return doc.children


def _returns_formatter(field, description):
    """Derive heads and tail from ``@returns`` blocks."""
    types = _or_types(field)
    tail = ('**%s** -- ' % types) if types else ''
    tail += description
    return ['returns'], tail


def _params_formatter(field, description):
    """Derive heads and tail from ``@param`` blocks."""
    heads = ['param']
    types = _or_types(field)
    if types:
        heads.append(types)
    heads.append(rst.escape(field['name']))
    tail = description
    return heads, tail


def _exceptions_formatter(field, description):
    """Derive heads and tail from ``@throws`` blocks."""
    heads = ['throws']
    types = _or_types(field)
    if types:
        heads.append(types)
    tail = description
    return heads, tail


def _or_types(field):
    """Return all the types in a doclet subfield like "params" or "returns"
    with vertical bars between them, like "number|string".

    ReST-escape the types.

    """
    return rst.escape('|'.join(field.get('type', {}).get('names', [])))


def _dotted_path(segments):
    """Convert a LUA object path (``['dir/', 'file/', 'class#',
    'instanceMethod']``) to a dotted style that Sphinx will better index."""
    segments_without_separators = [s[:-1] for s in segments[:-1]]
    segments_without_separators.append(segments[-1])
    return '.'.join(segments_without_separators)
