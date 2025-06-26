-- HW 1. Crear la base de datos
DROP DATABASE IF EXISTS market_db;
CREATE DATABASE market_db;

\c market_db;
-- HW 2.Modelado de Datos
-- Crear las siguientes tablas con relaciones:


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

-- Definir claves primarias (PK), foráneas (FK) y restricciones (ON DELETE CASCADE/SET NULL).