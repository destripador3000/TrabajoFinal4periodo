-- Estructura de tabla para la tabla `estudiante`
CREATE TABLE IF NOT EXISTS estudiante (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Estructura de tabla para la tabla `gestion_prestamo`
CREATE TABLE IF NOT EXISTS gestion_prestamo (
    id_estudiante INTEGER NOT NULL,
    id_prestamo INTEGER NOT NULL,
    FOREIGN KEY (id_estudiante) REFERENCES estudiante(id),
    FOREIGN KEY (id_prestamo) REFERENCES prestamo(id)
);

-- Estructura de tabla para la tabla `libro`
CREATE TABLE IF NOT EXISTS libro (
    id INTEGER PRIMARY KEY,
    codigo INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    autor TEXT NOT NULL
);

-- Estructura de tabla para la tabla `multa`
CREATE TABLE IF NOT EXISTS multa (
    id INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL,
    id_prestamo INTEGER NOT NULL,
    FOREIGN KEY (id_prestamo) REFERENCES prestamo(id)
);

-- Estructura de tabla para la tabla `prestamo`
CREATE TABLE IF NOT EXISTS prestamo (
    id INTEGER PRIMARY KEY,
    id_libro INTEGER NOT NULL,
    FOREIGN KEY (id_libro) REFERENCES libro(id),
    fecha DATE
);

-- Estructura de tabla para la tabla `usuario`
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY,
    codigo INTEGER NOT NULL,
    password TEXT NOT NULL
);
