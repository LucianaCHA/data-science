with data as (
    select current_date as input
    union all
    select current_date - interval '1 day'
    union all
    select current_date + interval '1 day'
    union all
    select null
),
result as (
    select
        input,
        {{ is_valid_date('input') }} as is_valid
    from data
)
select *
from result
where
    (input <= current_date and is_valid is not true) or
    (input > current_date and is_valid is not false) or
    (input is null and is_valid is not false)
