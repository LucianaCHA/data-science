-- tests/test_valid_status.sql

with data as (
    select 'enviado' as status
    union all
    select 'pendiente'
    union all
    select 'otro_estado'
)

select *
from data
where not {{ is_valid_status('status') }}