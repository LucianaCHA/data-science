-- Tarea 1: Productos con precio mayor al promedio general

SELECT productcode, productline, productname, priceeach
FROM sales
WHERE priceeach > (
    SELECT AVG(priceeach)
    FROM sales
);
