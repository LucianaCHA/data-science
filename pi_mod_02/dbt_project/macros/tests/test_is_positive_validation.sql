with data as (
    select 10 as input
    union all
    select 0
    union all
    select -5
    union all
    select null
),
result as (
    select input, {{ is_positive('input') }} as is_valid
    from data
)
select *
from result
where
    (input > 0 and is_valid is not true) or
    (input <= 0 and is_valid is not false) or
    (input is null and is_valid is not false)
