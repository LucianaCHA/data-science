with source as (

    select * from {{ source('public', 'users') }}

),

renamed as (

    select
        "UsuarioID" as user_id,
        initcap(trim("Nombre"))   as first_name,
        initcap(trim("Apellido")) as last_name,
        trim("DNI") as national_id,
        lower(trim("Email")) as email,
        "FechaRegistro"  as registration_date

        case 
            when lower(trim("Email")) ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' then true
            else false
        end as is_email_valid

    from source

)

select * from renamed