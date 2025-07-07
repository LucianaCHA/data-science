-- HW 1. Crear la base de datos
DROP DATABASE IF EXISTS market_db;
CREATE DATABASE market_db;

\c market_db;
-- HW 2.Modelado de Datos creaci{on de tablas

-- sucursales (id, nombre, ubicación)
CREATE TABLE branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL
);

-- productos (id, nombre, categoría, precio, stock, sucursal_id)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE SET NULL
);


-- clientes (id, nombre, email, fecha_registro)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    registration_date DATE NOT NULL
);
-- ventas (id, cliente_id, producto_id, fecha_venta, cantidad, total)
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    customer_id INT,
    product_id INT,
    sale_date DATE NOT NULL,
    quantity INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- Query para insertar datos de prueba
INSERT INTO branches (name, location) VALUES
('Sucursal Centro', 'Calle Principal 123'),
('Sucursal Norte', 'Avenida Norte 456'),
('Sucursal Sur', 'Calle Sur 789');

INSERT INTO products (name, category, price, stock, branch_id) VALUES
('Producto A', 'Categoría 1', 10.00, 100, 1),
('Producto B', 'Categoría 2', 20.00, 50, 1),
('Producto C', 'Categoría 1', 15.00, 200, 2),
('Producto D', 'Categoría 3', 30.00, 75, 3);

INSERT INTO customers (name, email, registration_date) VALUES
('Cliente 1', 'elmail@mail.com', '2023-01-01'),
('Cliente 2', 'un_mail@gmail.com', '2023-02-01'),

INSERT INTO sales (customer_id, product_id, sale_date, quantity, total) VALUES
(1, 1, '2023-03-01', 2, 20.00),
(2, 2, '2023-03-02', 1, 20.00),
(1, 3, '2023-03-03', 3, 45.00);

-- Query con un JOIN 
SELECT customers.name AS name, products.name AS product , sale_date, quantity, total, branches.name AS branch
FROM sales s
JOIN customers ON s.customer_id = customers.id
JOIN products ON s.product_id = products.id
JOIN branches ON products.branch_id = branches.id
ORDER BY customers.name, sale_date DESC;

-- update de precio de un producto
 UPDATE products
 SET price = price * 1.10}
 WHERE LOWER(category) = LOWER('category Name');


-- query para borrar un producto
DELETE FROM products
WHERE id = 1;

-- query para borrar un cliente
DELETE FROM customers
WHERE id = 1;

--buscar un cliente por email 
SELECT * FROM customers
WHERE email ILIKE 'el_email@para-buscar'

-- crear indice para la tabla de clientes para consultar por email

CREATE INDEX idx_customers_email ON customers(email);

-- crear un trigger para actualizar el stock de productos después de una venta
CREATE TRIGGER trg_update_stock_after_sale
AFTER INSERT ON {cls.table}
FOR EACH ROW
EXECUTE FUNCTION update_stock_after_sale();