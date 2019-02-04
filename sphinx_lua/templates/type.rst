{%- if type.id == "userdata" -%}
    userdata
{%- elif type.id == "any" -%}
    any
{%- elif type.id == "thread" -%}
    thread
{%- elif type.id == "boolean" -%}
    boolean
{%- elif type.id == "table" -%}
    table
{%- elif type.id == "function" -%}
    function
{%- elif type.id == "number" -%}
    number
{%- elif type.id == "string" -%}
    str
{%- elif type.id == "nil" -%}
    nil
{%- elif type.id == "custom" -%}
    {{ type.name }}
{%- elif type.id == "or" -%}
{% for type in type.types -%}
{% include "type.rst" %}{{ " or " if not loop.last }}
{%- endfor %}
{%- elif type.id == "dict" -%}
    dict[{% with type=type.key_type %}{% include "type.rst" %}{% endwith %}, {% with type=type.value_type %}{% include "type.rst" %}{% endwith %}]
{%- elif type.id == "array" -%}
    list[{% with type=type.type %}{% include "type.rst" %}{% endwith %}]
{%- elif type.id == "callable" -%}
    fun(
    {%- for type in type.arg_types -%}{% include "type.rst" %}{{ ", " if not loop.last }}{%- endfor -%}
    )
    {%- if type.return_types -%}
    :
    {%- endif -%}
    {%- for type in type.return_types -%}{% include "type.rst" %}{{ ", " if not loop.last }}{%- endfor -%}
{%- endif -%}