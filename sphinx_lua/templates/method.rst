{%- if method.is_static -%}
.. lua:staticmethod::
{%- else -%}
.. lua:method::
{%- endif -%}
{{ " " + method.name }}({% with function=method %}{% include "param_list.rst" %}{% endwith -%})
{%- filter indent(width=4) %}
{% if method.is_virtual -%}
:virtual:
{% endif -%}
{% if method.is_abstract -%}
:abstract:
{% endif -%}
{% if method.is_deprecated -%}
:deprecated:
{% endif -%}
{% if method.visibility == "protected" -%}
:protected:
{%- endif %}

{% if method.short_desc -%}
{{ method.short_desc | process_link }}
{% endif %}
{% if method.desc -%}
{{ method.desc | process_link }}
{%- endif %}

{% for param in method.params -%}
{%- with type=param.type -%}
{%- if param.name == "..." -%}
:param vararg: {{ param.desc|process_link }}
:type vararg: {% include "type.rst" %}
{% else -%}
:param {{ param.name }}: {{ param.desc|process_link }}
:type {{ param.name }}: {% include "type.rst" %}
{% endif -%}
{% endwith -%}
{%- endfor -%}

{% for return in method.returns -%}
{% with type=return.type %}
{%- if return.desc -%}
:return: {{ return.desc }}
{%- endif %}
:rtype: {% include "type.rst" %}
{% endwith %}
{%- endfor -%}

{%- if method.usage %}
**Usage:**

.. code-block:: lua
    :linenos:

    {{ method.usage|indent(4) }}
{% endif %}

{% if 'show-source' in options %}
.. container:: toggle

    .. literalinclude:: {{ file_path }}
        :language: lua
        :lines: {{ method|start_stop_line(file_path) }}

{% endif %}
{%- endfilter %}