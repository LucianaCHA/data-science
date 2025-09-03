with source as (

    select * from {{ source('public', 'products') }}

),

renamed as (

    select
        "ProductoID" as product_id,
        initcap(trim("Nombre"))   as product_name,
        initcap(trim("Descripcion")) as product_description,
        "Precio" as price,
        "Stock" as stock,
        "CategoriaID" as category_id
        case 
            when "Precio" >= 0 then true
            else false
        end as is_price_valid
        case 
            when "Stock" <= 0 then true
            else false
        end as out_of_stock

    from source

)

select * from renamed