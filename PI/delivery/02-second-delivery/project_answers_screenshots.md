# Preguntas y respuestas ENTREGABLE 2

## Trigger
1. Crea un trigger que registre en una tabla de monitoreo cada vez que un producto supere las 200.000 unidades vendidas acumuladas.

El trigger debe activarse después de insertar una nueva venta y registrar en la tabla el ID del producto, su nombre, la nueva cantidad total de unidades vendidas, y la fecha en que se superó el umbral.

**Solución** 

__Se creó tabla de auditoria en la base de datos ya existente:__ 

(en el contexto de la aplicación el [`script`](../../scripts/02_init_monitoring_table.sql) de creación es ejecutado luego del de creación de la base de datos [`sales_company`](../../scripts/01_init_db.sql) )
```sql
USE sales_company;

DROP TABLE IF EXISTS product_monitoring;
CREATE TABLE product_monitoring (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    ProductName VARCHAR(255),
    TotalSold INT,
    ThresholdDate DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
__Comando sql para crear trigger solicitado__


```sql
DELIMITER $$
CREATE TRIGGER trigger_product_threshold_200k --nombre del trigger
AFTER INSERT ON sales -- cuado se ejecuta? luego de cada insert en la tabla sales
FOR EACH ROW
BEGIN
    DECLARE total_sales INT; 
    -- setea en la variable declarada a partir de la sumatoria de la columna quantity de la tabla sales para el producto que se acaba de insertar
    SELECT SUM(Quantity)
    INTO total_sales
    FROM sales
    WHERE ProductID = NEW.ProductID;

    IF total_sales > 200000 THEN
    -- si el total de ventas es mayor a doscientos mil, se verifica si ya existe un registro de sobrepaso para el producto recién ingresado y si no existe , se inserta registro de auditoria
        IF NOT EXISTS (
            SELECT 1 FROM product_monitoring
            WHERE ProductID = NEW.ProductID
        ) THEN
            INSERT INTO product_monitoring (
                ProductID,
                productName,
                TotalSold
            )
            -- el select recupera la info que se insertará en la tabla de auditoria (product_monitoring) a partir de la tabla prodctos y del total de venas guardado como variable
            SELECT 
                ProductID,
                ProductName,
                total_sales
            FROM products
            WHERE p.ProductID = NEW.ProductID;
        END IF;
    END IF;

END$$

DELIMITER ;
```


**NOTA** El trigger se ejecuta con cada inserción en la tabla sales. Por eso se decidió ejecutar su creación a posteriori de la carga inicial de datos, para evitar ejecuciones innecesarias durante el poblamiento inicial de la base.
En el contexto de este proyeccto la creación , tanto del trigger como de la tabla de monitoreo, sucede durante la inicialización del mismo

##  Registro
Registra una venta correspondiente al vendedor con ID 9, al cliente con ID 84, del producto con ID 103, por una cantidad de 1.876 unidades y un valor de 1200 unidades.

Consulta la tabla de monitoreo, toma captura de los resultados y realiza un análisis breve de lo ocurrido.


Dado que la tabla sales no cuenta con una clave primaria autoincremental, el valor de salesID se define dinámicamente a partir del valor máximo existente. Esta práctica, aunque funcional, no es adecuada en escenarios concurrentes, ya que existe riesgo de colisión de claves. En entornos productivos, la clave primaria debería ser un campo autoincremental para garantizar unicidad.


```sql
INSERT INTO sales (salesID, salesPersonID, customerID, productID, quantity, totalPrice, salesDate)
SELECT 
    COALESCE(MAX(salesID), 0) + 1,
    9,
    84,
    103,
    1876,
    1200,
    '2025-06-10 10:00:00'
FROM sales;
```

Comando sql con consulta  __product_monitoring__ donde se comprueba creación de un nuevo registro (cumplidos los parametros del trigger )

```sql
SELECT * FROM product_monitoring
WHERE productID = 103;
```

**Resultado:**

![resgitro_monitoring](/PI/assets/01-images/register.png)


**Análisis** :
El registro insertado provocó que el acumulado de unidades vendidas para el producto con ID 103 superara el umbral de 200.000 unidades. Dado que esta es la condición definida para la activación del trigger __trigger_product_threshold_200k__, el mismo trigger se ejecutó automáticamente. Como resultado, se insertó un registro en la tabla de auditoría __product_monitoring__ con los datos correspondientes al producto. Este comportamiento ocurrió de forma transparente para el usuario, evidenciando el funcionamiento correcto del trigger ante el cumplimiento de la condición

## Optimización

1. Selecciona dos consultas del avance 1 y crea los índices que consideres más adecuados para optimizar su ejecución.

2. Prueba con índices individuales y compuestos, según la lógica de cada consulta. Luego, vuelve a ejecutar ambas consultas y compara los tiempos de ejecución antes y después de aplicar los índices. Finalmente, describe brevemente el impacto que tuvieron los índices en el rendimiento y en qué tipo de columnas resultan más efectivos para este tipo de operaciones.

### **1)** Query 1 (~12 segundos en entorno kernel).

-- La siguiente consulta calcula:

* los 5 productos más vendidos (top_products).

* Para cada uno, se agrupan las ventas por vendedor y se calcula volumen individual de ventas (seller_sales).

* Ranking de cada vendedor por producto en función del total vendido, para luego obtener el top 1 de cada producto (ranked_sellers).


```sql
WITH top_products AS (
    SELECT 
        p.productID AS product_id,
        p.productName AS product_name,
        SUM(s.quantity) AS total_quantity
    FROM products p
    JOIN sales s ON p.productID = s.productID
    GROUP BY p.productID, p.productName
    ORDER BY total_quantity DESC
    LIMIT 5
),
seller_sales AS (
    SELECT 
        tp.product_id,
        tp.product_name,
        tp.total_quantity AS total_sold,
        s.salesPersonID AS seller_id,
        SUM(s.quantity) AS seller_quantity
    FROM top_products tp
    JOIN sales s ON tp.product_id = s.productID
    GROUP BY tp.product_id, tp.product_name, s.salesPersonID
),
ranked_sellers AS (
    SELECT 
        *,
        RANK() OVER (PARTITION BY product_id ORDER BY seller_quantity DESC) AS seller_rank
    FROM seller_sales
)
SELECT 
    rs.product_id,
    rs.product_name,
    rs.seller_id,
    rs.total_sold,
    CONCAT( e.FirstName ,' ', e.LastName) AS seller_name,
    rs.seller_quantity
FROM ranked_sellers rs
JOIN employees e ON rs.seller_id = e.employeeID
WHERE seller_rank = 1
ORDER BY seller_quantity DESC;
```

**Tiempo de ejecución previo a uso de index
:**
![before_index](/PI/assets/01-images/time_before_index.png)



**EXPLAIN**
![explain_before_index](/PI/assets/01-images/explain_before_index.png)



* Índices aplicados
Se crearon índices para optimizar JOIN, GROUP BY y ORDER BY  que son las más costosas

```sql
-- products: la clave usada en JOIN y GROUP BY 
CREATE INDEX idx_products_productID_name ON products(productID, productName);

-- sales: combinando JOIN + WHERE + agregación
CREATE INDEX idx_sales_productID_salesPersonID_quantity ON sales(productID, salesPersonID, quantity);
```

**Resultado**
![time_after_index](/PI/assets/01-images/time_after_index.png)


![explain_after_index](/PI/assets/01-images/explain_after_index.png)


### Impacto observado

Tras la aplicación de los índices:

* El tiempo de ejecución se redujo en casi un 75%.

* Se evitan full scan en las tablas sales y products, mediante el uso de índices.
* Agregación y ordenamiento se benefician del uso de índices compuestos que combinan las columnas más utilizadas.


## **2)** Query 2 (~15 segundos en entorno kernel).

La siguiente consulta calcula:
* los 5 productos más vendidos (top_products). 
* Para esos productos, se cuentan la cantidad de clientes únicos que compraron dichos productos (customer_counts).
* Sumatoria de clientes (total_customers).
* Porcentaje de clientes únicos que compraron cada producto top respecto al total.


```sql
WITH top_products AS (
    SELECT 
        p.productID AS product_id,  
        p.productName AS product_name,
        SUM(s.quantity) AS total_quantity
    FROM products p
    JOIN sales s ON p.productID = s.productID
    GROUP BY p.productID, p.productName
    ORDER BY total_quantity DESC
    LIMIT 5
),
customer_counts AS (
    SELECT
        tp.product_id,
        COUNT(DISTINCT s.customerID) AS unique_customers
    FROM top_products tp
    JOIN sales s ON tp.product_id = s.productID
    GROUP BY tp.product_id
),
total_customers AS (
    SELECT COUNT(DISTINCT customerID) AS total_customers
    FROM sales
)
SELECT
    cc.product_id,
    tp.product_name,
    cc.unique_customers,
    tc.total_customers,
    ROUND((cc.unique_customers/ tc.total_customers) * 100, 2) AS proportion_percentage
FROM customer_counts cc
JOIN top_products tp ON cc.product_id = tp.product_id
JOIN total_customers tc ON true
ORDER BY cc.unique_customers DESC;
```

**Tiempo de ejecución previo a uso de index
:**
![before_index](/PI/assets/01-images/time_before_index_2.png)



**EXPLAIN**
![explain_before_index_2](/PI/assets/01-images/explain_before_index_2.png)



* Índices aplicados
Se crearon los siguientes índices para optimizar las cláusulas JOIN, GROUP BY y ORDER BY que generaban cuellos de botella. En comentarios se especifica sobre qué subconsulta/tabla se espera mejorar la consulta con el ìndice.



```sql
-- para subconsulta top_products
-- El JOIN entre products y sales requiere escanear muchas filas 
CREATE INDEX idx_sales_productID_quantity ON sales(productID, quantity);

-- Subconsulta customer_counts
-- Para filtrar por productID y agrupar por customerID y evitar scanearde nuevo toda la tabla sales 
CREATE INDEX idx_sales_productID_customerID ON sales(productID, customerID);

--Subconsulta total_customers , implica barrer toda la base 
CREATE INDEX idx_sales_customerID ON sales(customerID);

```

**Resultado**

![time_after_index_2](/PI/assets/01-images/time_after_index_2.png)


![explain_after_index_2](/PI/assets/01-images/explain_after_index_2.png)


### Impacto observado

Tras la creación de los índices, 
* El tiempo de ejecución se redujo casi 5 veces (~3 segundos en entorno kernel). 

* Explain muestra que planea usar los índices creados en casi todos los joins y filtros, lo cual es muy relevante dado que son las operaciones potencialmente más costosas.

* La tabla sales ahora usa range y ref en lugar de ALL, cuyo significa un scaneo de toda la tabla.
* Los índices idx_sales_customerID e idx_sales_productID_customerID están 
tp.product_id reduce a 5 filas, lo cual permite joins màs rápidos y precisos (dado que son menos elementos)



# **Resumen**

Tras aplicar ìndices, se comprobó con EXPLAIN:

* Los mismos fueron utilizados correctamente (Using index).

* Se redujo el costo de acceso a las tablas principales.

* Persisten operaciones de ordenamiento costosas (Using temporary, Using filesort), debido a la lógica de agregación, ranking y limitación de resultados que no se benefician inmediatamente con los índices. Se podrían explorar mejoras en las consultas como evitar LIMIT y ORDER en las subconsultas .


