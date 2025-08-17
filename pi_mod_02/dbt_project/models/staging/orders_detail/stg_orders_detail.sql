with source as (

    select * from {{ source('public', 'orders_detail') }}

),

validated as (

    select
        "DetalleID" as order_detail_id,
        "OrdenID" as order_id,
        "ProductoID" as product_id,
        "Cantidad" as quantity,
        "PrecioUnitario" as unit_price,
        {{is_positive('"Cantidad"') }} as is_valid_quantity,
        {{is_positive('"PrecioUnitario"') }} as is_valid_unit_price,
        "Cantidad" * "PrecioUnitario" as total_price,
    from source

)

select * from validated
