
.. lua:class:: {{ name }}

   {% for function in model.methods -%}
    .. lua:method:: {{ function.name }}({% include "param_list.rst" %})

        {{ function.short_desc }}
        {{ function.desc }}

        {% for param in function.params -%}
        {% with model=param %}
        :param {% include "type.rst" %} {{ param.name }}: {{ param.desc }}
        {% endwith %}
        {%- endfor %}

        {% for return in function.returns -%}
        {% with model=return %}
        :return: {{ return.name }}: {{ return.desc }}
        :rtype: {% include "type.rst" %}
        {% endwith %}
        {%- endfor %}

   {% endfor %}
