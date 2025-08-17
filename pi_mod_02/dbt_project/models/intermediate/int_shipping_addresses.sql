with base as (
    select
        address_id,
        user_id,
        street,
        district,
        state,
        zip_code,
        department,
        country,
        province,
        city
    from {{ ref('stg_shipping_addresses') }}
),

countries as (
    select * from {{ ref('dim_country') }}
),

provinces as (
    select * from {{ ref('dim_province') }}
),

cities as (
    select * from {{ ref('dim_city') }}
),

location_with_keys as (
    select
        base.address_id,
        base.user_id,
        base.street,
        base.district,
        base.state,
        base.zip_code,
        base.department,
        c.country_id,
        p.province_id,
        ci.city_id
    from base
    left join countries c
        on base.country = c.country
    left join provinces p
        on base.province = p.province
        and base.country = p.country
    left join cities ci
        on base.city = ci.city
        and base.province = ci.province
        and base.country = ci.country
)

select * from location_with_keys
