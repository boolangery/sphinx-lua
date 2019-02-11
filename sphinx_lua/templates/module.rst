.. lua:module:: {{ module.name }}

{{ module.short_desc|process_link if module.short_desc }}

{{ module.desc|process_link if module.desc }}

{% if module.usage -%}
**Usage:**

.. code-block:: lua
    :linenos:

    {{ module.usage|indent(4) }}
{%- endif %}

{% for function in module.functions %}
{% include "function.rst" %}
{% endfor %}

{% for model in module.classes %}
{% include "class.rst" %}
{% endfor %}
