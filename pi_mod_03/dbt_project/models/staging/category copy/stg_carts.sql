with source as (

    select * from {{ source('public', 'carts') }}

),

staged_carts as (

    select
        "CarritoID" as category_id,
        "UsuarioID" as user_id,
        "ProductoID" as product_id,
        "Cantidad" as quantity,
        "FechaAgregado" as added_date,
        {{ is_positive('"Cantidad"') }} as is_valid_quantity,
        
    from source

)

select * from staged_carts