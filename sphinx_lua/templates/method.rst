.. lua:method:: {{ method.name }}({% with function=method %}{% include "param_list.rst" %}{% endwith -%})
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
{{ method.short_desc }}
{%- endif -%}

{% if method.desc -%}
{{ method.desc }}
{%- endif %}

{% if method.usage %}
.. code-block:: lua
    :linenos:

    {{ method.usage }}
{% endif %}

{% for param in method.params -%}
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

{% for return in method.returns -%}
{% with type=return.type %}
:return: {{ return.desc }}
:rtype: {% include "type.rst" %}
{% endwith %}
{%- endfor %}
{%- endfilter %}