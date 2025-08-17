with order_details as (
    select * from {{ ref('int_orders_detail') }}
),

orders as (
    select * from {{ ref('int_orders') }}
),

users as (
    select * from {{ ref('dim_users') }}
),

products as (
    select * from {{ ref('dim_products') }}
),

locations as (
    select * from {{ ref('int_shipping_addresses') }}
),

fact_base as (
    select
        od.order_detail_id,
        o.order_id,
        o.order_date,
        u.user_id,
        p.product_id,
        od.quantity,
        od.unit_price,
        od.quantity * od.unit_price as total_amount,
        o.method_payment_id,
        loc.city_id,
        loc.province_id,
        loc.country_id
    from order_details od
    join orders o on od.order_id = o.order_id
    join users u on o.user_id = u.user_id
    join products p on od.product_id = p.product_id
    left join locations loc on u.address_id = loc.address_id -- o como corresponda
)

select * from fact_base
