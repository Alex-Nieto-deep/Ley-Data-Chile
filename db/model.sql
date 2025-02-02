CREATE TABLE leyes_chile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_proyecto TEXT NOT NULL,
    fecha_ingreso TEXT NOT NULL,
    iniciativa TEXT NOT NULL,
    proyecto_suma REAL NOT NULL,
    numero_ley TEXT NOT NULL,
    fecha_publicacion TEXT NOT NULL,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE leyes_chile_temas_principales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_ley TEXT NOT NULL,
    materias TEXT NOT NULL,
    resumen TEXT NOT NULL,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (numero_ley) REFERENCES leyes_chile(numero_ley) ON DELETE CASCADE ON UPDATE CASCADE
);