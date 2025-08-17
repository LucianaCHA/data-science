with source as (

    select * from {{ source('public', 'orders') }}

),

validated as (

    select
        "OrdenID" as order_id,
        "UsuarioID" as user_id,
        "FechaOrden" as order_date,
        "Total" as total,
        {{is_positive('"Total"') }} as is_valid_total,

        -- case 
        --     when "Total" is not null and "Total" > 0 then true
        --     else false
        -- end as is_valid_total,

        {{is_valid_status('"Estado"') }} as is_valid_status,
        {{translate_status('"Estado"') }} as order_status

    from source

)

select * from validated
