{%- for param in function.params -%}
{%- if param.is_opt -%}{% set close_brack = True %}[{%- endif -%}
{{ param.name }}
{%- if not loop.last -%}, {%- elif close_brack -%}]{%- endif -%}
{%- endfor -%}