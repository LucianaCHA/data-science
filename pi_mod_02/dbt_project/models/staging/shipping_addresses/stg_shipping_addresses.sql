with source as (

    select * from {{ source('public', 'shipping_addresses') }}

),

validated as (

    select
        "DireccionID" as address_id,
        "UsuarioID" as user_id,
        {{ clean_text('"Calle"') }} as street,
        {{ clean_text('"Ciudad"') }} as city,
        {{ clean_text('"Provincia"') }} as province,
        {{ clean_text('"Distrito"') }} as district,
        {{ clean_text('"Estado"') }} as state,
        {{ clean_text('"CodigoPostal"') }} as zip_code,
        {{ clean_text('"Pais"') }} as country,
        {{ clean_text('"Departamento"') }} as department,
    from source

)

select * from validated
