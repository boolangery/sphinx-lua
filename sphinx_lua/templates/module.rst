.. lua:module:: {{ module.name }}
{% for function in module.functions %}
{% include "function.rst" %}
{% endfor %}

{% for model in module.classes %}
{% include "class.rst" %}
{% endfor %}
