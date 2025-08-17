with source as (

    select * from {{ source('public', 'categories') }}

),

staged_categories as (

    select
        "CategoriaID" as category_id,
        initcap(trim("Nombre")) as category_name,
        initcap(trim("Descripcion")) as category_description
    from source

)

select * from staged_categories