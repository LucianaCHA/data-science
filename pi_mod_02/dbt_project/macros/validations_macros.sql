{% macro is_positive(column_name) %}
    case
        when {{ column_name }} is not null and {{ column_name }} > 0 then true
        else false
    end
{% endmacro %}

{% macro is_valid_status(column_name) %}
    case
        when {{ clean_text(column_name) }} in ('enviado', 'completado', 'cancelado', 'pendiente') then true
        else false
    end
{% endmacro %}

{% macro is_valid_date(column_name) %}
    case
        when {{ column_name }} is not null and {{ column_name }} <= current_date then true
        else false
    end
{% endmacro %}