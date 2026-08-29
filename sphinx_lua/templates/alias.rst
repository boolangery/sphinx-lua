.. lua:alias:: {{ model.name }} = {% with type=model.type %}{% include "type.rst" %}{% endwith %}

{{ model.desc|process_link if model.desc }}
