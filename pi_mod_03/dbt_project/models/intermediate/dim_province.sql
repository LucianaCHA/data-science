with base as (
    select distinct
        province,
        country
    from {{ ref('stg_shipping_addresses') }}
),

joined as (
    select
        {{ dbt_utils.surrogate_key(['province', 'country']) }} as province_id,
        p.province,
        p.country,
        c.country_id
    from base p
    join {{ ref('dim_country') }} c
    on p.country = c.country
)

select * from joined
