with base as (
    select distinct
        city,
        province,
        country
    from {{ ref('stg_shipping_addresses') }}
),

joined as (
    select
        {{ dbt_utils.surrogate_key(['city', 'province', 'country']) }} as city_id,
        b.city,
        b.province,
        b.country,
        p.province_id
    from base b
    join {{ ref('dim_provinces') }} p
    on b.province = p.province and b.country = p.country
)

select * from joined
