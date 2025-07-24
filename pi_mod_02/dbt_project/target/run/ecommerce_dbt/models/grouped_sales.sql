
  create view "ecommerce_db"."public"."grouped_sales__dbt_tmp"
    
    
  as (
    -- models/ventas_agrupadas.sql

SELECT * FROM "Usuarios" LIMIT 10
  );