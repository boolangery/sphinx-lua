.. lua:function::
{{- " " + function.name }}({%- include "param_list.rst" %})
{%- filter indent(width=4) %}

{% if function.short_desc -%}
{{ function.short_desc }}
{% endif %}
{% if function.desc -%}
{{ function.desc }}
{%- endif %}

{% for param in function.params -%}
{%- with type=param.type -%}
{%- if param.name == "..." -%}
:param vararg: {{ param.desc }}
:type vararg: {% include "type.rst" %}
{% else -%}
:param {{ param.name }}: {{ param.desc }}
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
