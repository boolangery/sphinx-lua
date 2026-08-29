.. lua:alias:: {{ model.name }} = {% with type=model.type %}{% include "type.rst" %}{% endwith %}

{{ model.desc|render_code_fences|process_link if model.desc }}
