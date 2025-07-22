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