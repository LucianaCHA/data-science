with base as (
    select distinct country
    from {{ ref('stg_shipping_addresses') }}
),

with_id as (
    select
        {{ dbt_utils.surrogate_key(['country']) }} as country_id,
        country
    from base
)

select * from with_id