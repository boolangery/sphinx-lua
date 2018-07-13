
.. lua:class:: {{ name }}

   {% for function in model.methods -%}
    .. lua:method:: {{ function.name }}({{ function.params|join(', ', attribute='name') }})

        {% for param in function.params -%}
        :param {% include "type.rst" %} {{ param.name }}: {{ param.desc }}

        {% endfor %}

   {% endfor %}
