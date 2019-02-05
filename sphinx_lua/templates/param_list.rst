{%- for param in function.params -%}
{%- if param.is_opt -%}{%- endif -%}
{{ param.name }}{{ "=" + param.default_value if param.default_value }}{{ ", " if not loop.last }}
{%- endfor -%}