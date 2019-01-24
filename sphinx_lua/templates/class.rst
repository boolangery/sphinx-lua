.. lua:class:: {{ name }}

    {{ model.desc|indent(4) }}
    {{ model.usage|indent(4) }}

    {% for function in model.methods -%}
    {% if function.visibility != 2 %}
    .. lua:method:: {{ function.name }}({% include "param_list.rst" %})
        {% if function.is_virtual %}:virtual:{% endif -%}
        {% if function.is_abstract %}:abstract:{% endif -%}
        {% if function.is_deprecated %}:deprecated:{% endif %}

        {{ function.short_desc|indent(8) }}

        {{ function.desc|indent(8) }}

        {% if function.usage %}
        .. code-block:: lua
           :linenos:

           {{ function.usage|indent(12) }}
        {% endif %}

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
    {% endif %}
    {% endfor %}
