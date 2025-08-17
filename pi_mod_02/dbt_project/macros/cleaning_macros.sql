{% macro clean_text(column_name) %}
    lower(trim({{ column_name }}))
{% endmacro %}