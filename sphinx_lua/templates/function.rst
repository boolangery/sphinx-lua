.. lua:function::
{{- " " + function.name }}({%- include "param_list.rst" %})
{%- filter indent(width=4) %}

{% if function.short_desc -%}
{{ function.short_desc | process_link }}
{% endif %}
{% if function.desc -%}
{{ function.desc | process_link }}
{%- endif %}

{% for param in function.params -%}
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

{% for return in function.returns -%}
{% with type=return.type %}
{%- if return.desc -%}
:return: {{ return.desc }}
{%- endif %}
:rtype: {% include "type.rst" %}
{% endwith %}
{%- endfor -%}

{%- if function.usage %}
**Usage:**

.. code-block:: lua
    :linenos:

    {{ function.usage|indent(4) }}
{% endif %}

{%- endfilter %}
