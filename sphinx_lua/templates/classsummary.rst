.. list-table::
    :header-rows: 1

    * - Class
      - Description
    {% for class in model|sort(attribute='name') %}
    * - :lua:class:`{{ class.name }}`
      - {{ class.desc[:70]|replace('\n', '') }}{{ "..." if class.desc|length > 70 }}
    {% endfor %}
