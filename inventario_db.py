# ======================================================================
#                      BASE DE DATOS - PRODUCTOS
# ======================================================================
# Archivo:   inventario_db.py
# Alumna:    Melisa S. Rossi
# Docente:   Gabriel Feldman
# Tutora:    Sofía Tarabusi
# Curso:     Iniciación a la Programación con Python
# Trayecto:  2024 - Talento Tech
# ----------------------------------------------------------------------
# Descripción:
# Este archivo utiliza la librería sqlite3 para la gestión de la base de 
# datos del inventario de productos para una pequeña tienda. 
# ======================================================================

# Importar la librería sqlite3 para la gestión de bases de datos SQLite:
import sqlite3

# Conexión a la base de datos "inventario_msr.db" (se crea si no existe):
conexion = sqlite3.connect("inventario_msr.db")
cursor = conexion.cursor()

# Crear la tabla 'productos' si no existe:
# La tabla incluye:
#   - id: identificador único (autoincremental).
#   - nombre: nombre del producto (no nulo).
#   - descripcion: detalles del producto (no nulo).
#   - cantidad: cantidad disponible en stock (no nulo).
#   - precio: precio del producto (no nulo).
#   - categoria: categoría a la que pertenece el producto (no nulo).
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT    NOT NULL,
    descripcion TEXT    NOT NULL,
    cantidad    INTEGER NOT NULL,
    precio      REAL    NOT NULL,
    categoria   TEXT    NOT NULL
)
''')

# Guarda los cambios y cierra la conexión a la base de datos:
conexion.commit()
conexion.close()