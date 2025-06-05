
-- Tabla estudiantes
CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    estado VARCHAR(20) DEFAULT 'activo'
);

INSERT INTO estudiantes (nombre, email, estado) VALUES
('Sofía Ramírez', 'sofia@correo.com', 'activo'),
('Martín Gómez', 'martin@correo.com', 'activo'),
('Elena Torres', 'elena@correo.com', 'inactivo');

-- Tabla materias
CREATE TABLE materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    creditos INT
);

INSERT INTO materias (nombre, creditos) VALUES
('Matemática I', 6),
('Historia', 4),
('Programación', 8);

-- Tabla inscripciones
CREATE TABLE inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    materia_id INT,
    fecha DATE,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);

INSERT INTO inscripciones (estudiante_id, materia_id, fecha) VALUES
(1, 1, '2024-03-01'),
(1, 2, '2024-03-01'),
(2, 3, '2024-03-02');

-- Tabla calificaciones
CREATE TABLE calificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    materia_id INT,
    nota DECIMAL(4,2),
    fecha DATE,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);

INSERT INTO calificaciones (estudiante_id, materia_id, nota, fecha) VALUES
(1, 1, 8.5, '2024-04-01'),
(1, 2, 6.0, '2024-04-01'),
(2, 3, 9.0, '2024-04-01');

-- Tabla para auditoría (triggers)
CREATE TABLE auditoria_eliminaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    email VARCHAR(255),
    eliminado_en DATETIME
);
