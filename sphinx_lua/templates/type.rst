{%- if model.type.type == 1 -%}
    {{ model.type.name_if_custom }}
{%- else %}
{%- if model.type.type == 0 -%}
    unknow
{%- elif model.type.type == 2 -%}
    string
{%- elif model.type.type == 3 -%}
    number
{%- elif model.type.type == 4 -%}
    integer
{%- elif model.type.type == 5 -%}
    float
{%- elif model.type.type == 6 -%}
    boolean
{%- elif model.type.type == 7 -%}
    function
{%- elif model.type.type == 8 -%}
    table
{%- elif model.type.type == 9 -%}
    userdata
{%- endif -%}
{%- endif -%}