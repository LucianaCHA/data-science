-- Usuarios Report SQL
-- consulta clientes registrados por mes 
SELECT 
    DATE_TRUNC('month', "FechaRegistro") AS register_month, 
    COUNT(*) AS users 
FROM "Usuarios" 
GROUP BY register_month 
ORDER BY register_month

-- ¿Cuántos usuarios han realizado más de una orden?
SELECT 
    COUNT(DISTINCT "UsuarioID") AS users_with_multiple_orders
FROM "Ordenes"
WHERE "UsuarioID" IN (
    SELECT "UsuarioID"
    FROM "Ordenes"
    GROUP BY "UsuarioID"
    HAVING COUNT(*) > 1
);
--# ¿Qué usuarios han gastado más en total?
SELECT 
    "UsuarioID",
    SUM("Total") AS total_spent
FROM "Ordenes"
GROUP BY "UsuarioID"
ORDER BY total_spent DESC
LIMIT 10;

-- ¿Cuántos usuarios han dejado reseñas?
SELECT 
    COUNT(DISTINCT "UsuarioID") AS users_with_reviews
FROM "ReseñasProductos";


-- Report SQL - Productos
-- ¿Qué productos tienen alto stock pero bajas ventas?
SELECT 
    p."ProductoID",
    p."Nombre",
    p."Stock",
    COALESCE(SUM(d."Cantidad"), 0) AS total_vendido
FROM "Productos" p
LEFT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
GROUP BY p."ProductoID", p."Nombre", p."Stock"
ORDER BY p."Stock" DESC, total_vendido ASC
LIMIT 10;

-- # ranking de ventas por producto
SELECT 
    p."ProductoID",
    p."Nombre",
    p."Stock",
    COALESCE(SUM(d."Cantidad"), 0) AS total_vendido
FROM "Productos" p
LEFT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
GROUP BY p."ProductoID", p."Nombre", p."Stock"
HAVING p."Stock" >= 150 AND COALESCE(SUM(d."Cantidad"), 0) < 500
ORDER BY p."Stock" DESC;

-- Ordenar por stock decreciente los productos con menos de 500 ventas 
SELECT 
    p."ProductoID",
    p."Nombre",
    p."Stock",
    COALESCE(SUM(d."Cantidad"), 0) AS total_vendido
FROM "Productos" p
LEFT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
GROUP BY p."ProductoID", p."Nombre", p."Stock"
HAVING COALESCE(SUM(d."Cantidad"), 0) < 100
ORDER BY p."Stock" DESC
LIMIT 10;

-- ¿Cuántos productos están actualmente fuera de stock?
SELECT COUNT(*) AS total_out_of_stock
FROM "Productos"
WHERE "Stock" = 0;

-- ¿Cuáles son los productos peor calificados?

SELECT 
    p."ProductoID",
    p."Nombre",
    p."Stock",
    COALESCE(SUM(d."Cantidad"), 0) AS total_vendido,
    AVG(r."Calificacion") AS promedio_calificacion
FROM "Productos" p
LEFT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
LEFT JOIN "ReseñasProductos" r ON p."ProductoID" = r."ProductoID"
GROUP BY p."ProductoID", p."Nombre", p."Stock"
HAVING AVG(r."Calificacion") IS NOT NULL
ORDER BY promedio_calificacion ASC
LIMIT 10;

-- producto con mayor cantidad de reseñas 
SELECT 
    p."ProductoID",
    p."Nombre",
    COUNT(r."ReseñaID") AS total_reseñas
FROM "Productos" p
LEFT JOIN "ReseñasProductos" r ON p."ProductoID" = r."ProductoID"
GROUP BY p."ProductoID", p."Nombre"
ORDER BY total_reseñas DESC
LIMIT 10;

-- ¿Qué categoría tiene el mayor valor económico vendido (no solo volumen)?

SELECT 
    c."CategoriaID",
    c."Nombre" AS categoria,
    SUM(d."Cantidad" * p."Precio") AS valor_vendido
FROM "Categorias" c
JOIN "Productos" p ON c."CategoriaID" = p."CategoriaID"
LEFT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
GROUP BY c."CategoriaID", c."Nombre"
ORDER BY valor_vendido DESC
LIMIT 10;

-- ranking de categorías
SELECT 
    c."CategoriaID",
    c."Nombre" AS categoria,
    COUNT(d."Cantidad") AS total_vendido
FROM "Categorias" c
JOIN "Productos" p ON c."CategoriaID" = p."CategoriaID"
LEFT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
GROUP BY c."CategoriaID", c."Nombre"
ORDER BY total_vendido DESC
LIMIT 10;

-- Exploracion Ordenes
--¿Cuáles son los productos más vendidos por volumen?
SELECT 
    p."ProductoID",
    p."Nombre",
    SUM(d."Cantidad") AS total_vendido
FROM "Productos" p
RIGHT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
GROUP BY p."ProductoID", p."Nombre"
ORDER BY total_vendido DESC
LIMIT 10;

-- ¿Cuál es el ticket promedio por orden?
SELECT
    AVG("Total") AS ticket_promedio
    FROM "Ordenes";

-- ¿Cuáles son las categorías con mayor número de productos vendidos?

SELECT
    c."CategoriaID",
    c."Nombre" AS categoria,
    COUNT(d."Cantidad") AS total_vendido
FROM "Categorias" c
JOIN "Productos" p ON c."CategoriaID" = p."CategoriaID"
LEFT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
GROUP BY c."CategoriaID", c."Nombre"
ORDER BY total_vendido DESC
LIMIT 10;

-- Ventas por día de semana 
SELECT
    TO_CHAR("FechaOrden", 'Day') AS dia_semana,
    COUNT(*) AS total_ventas
FROM "Ordenes"
GROUP BY dia_semana
ORDER BY total_ventas DESC;

--Ordenes por mes 

SELECT
    DATE_TRUNC('month', "FechaOrden") AS mes,
    COUNT(*) AS total_ordenes
FROM "Ordenes"
GROUP BY mes
ORDER BY mes;


-- Exploración DetalleOrdenes
-- Número de ítems por orden
SELECT
    o."OrdenID",
    COUNT(d."DetalleID") AS total_items
FROM "Ordenes" o
JOIN "DetalleOrdenes" d ON o."OrdenID" = d."OrdenID"
GROUP BY o."OrdenID"
ORDER BY total_items DESC
LIMIT 10;

-- promedio de items por orden
SELECT
    AVG(total_items) AS promedio_items_por_orden
FROM (
    SELECT
        o."OrdenID",
        COUNT(d."DetalleID") AS total_items
    FROM "Ordenes" o
    JOIN "DetalleOrdenes" d ON o."OrdenID" = d."OrdenID"
    GROUP BY o."OrdenID"
) subquery;

-- Distribución de ítems por orden
SELECT
    "OrdenID",
    SUM("Cantidad") AS total_items
FROM "DetalleOrdenes"
GROUP BY "OrdenID";

