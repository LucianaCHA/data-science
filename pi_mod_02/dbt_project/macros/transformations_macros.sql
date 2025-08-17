{% macro translate_status(column_name) %}
    {% set cleaned_column_name = clean_text(column_name) %}
    case
        when {{ cleaned_column_name }} = 'enviado' then 'shipped'
        when {{ cleaned_column_name }} = 'completado' then 'completed'
        when {{ cleaned_column_name }} = 'cancelado' then 'cancelled'
        when {{ cleaned_column_name }} = 'pendiente' then 'pending'
        else null
    end
{% endmacro %}
