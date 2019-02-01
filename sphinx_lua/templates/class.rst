.. lua:class:: {{ name }}
{%- filter indent(width=4) %}

{% if model.desc -%}
    {{ model.desc }}
{%- endif -%}

{%- if model.desc -%}
    {{ model.usage }}
{%- endif -%}

{# display public methods first #}
{%- for method in model.methods -%}
{%- if method.visibility == "public" %}
{% include "method.rst" %}
{%- endif %}
{%- endfor %}

{# then display protected one #}
{%- for method in model.methods -%}
{%- if method.visibility == "protected" -%}
{%- include "method.rst"|indent(4) %}
{%- endif %}
{%- endfor %}
{%- endfilter %}
