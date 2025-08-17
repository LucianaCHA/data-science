with data as (
    select '  Enviado  ' as input
    union all
    select '  COMpletado'
),
result as (
    select {{ clean_text('input') }} as cleaned
    from data
)
select *
from result
where cleaned not in ('enviado', 'completado')
