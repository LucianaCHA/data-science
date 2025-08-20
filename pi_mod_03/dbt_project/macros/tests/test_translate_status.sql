with data as (
    select 'enviado' as status
    union all
    select 'completado'
    union all
    select 'cancelado'
    union all
    select 'pendiente'
    union all
    select 'otro'
),
result as (
    select
        status,
        {{ translate_status('status') }} as translated
    from data
)
select *
from result
where
    (status = 'enviado' and translated != 'shipped') or
    (status = 'completado' and translated != 'completed') or
    (status = 'cancelado' and translated != 'cancelled') or
    (status = 'pendiente' and translated != 'pending') or
    (status = 'otro' and translated is not null)
