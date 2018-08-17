
{{ model.usage }}

.. lua:class:: {{ name }}

    {{ model.desc|indent(4) }}

    {% for function in model.methods -%}
    .. lua:method:: {{ function.name }}({% include "param_list.rst" %})
        {% if function.is_virtual %}:virtual:{% endif -%}
        {% if function.is_abstract %}:abstract:{% endif -%}
        {% if function.is_deprecated %}:deprecated:{% endif %}

        {{ function.short_desc|indent(8) }}

        {{ function.desc|indent(8) }}

        {{ function.usage|indent(8) }}

        {% for param in function.params -%}
        {% with model=param %}
        :param {% include "type.rst" %} {{ param.name }}: {{ param.desc }}
        {% endwith %}
        {%- endfor %}

        {% for return in function.returns -%}
        {% with model=return %}
        :return: {{ return.desc }}
        :rtype: {% include "type.rst" %}
        {% endwith %}
        {%- endfor %}

    {% endfor %}
