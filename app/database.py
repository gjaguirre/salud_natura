import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "salud_natura.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Asegurar que el directorio padre de la base de datos exista
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS base_conocimiento_salud (
            id_remedio INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_remedio TEXT NOT NULL,
            planta_base TEXT,
            propiedades TEXT,
            contraindicaciones TEXT,
            dosificacion TEXT,
            link_articulo_web TEXT,
            imagen_url TEXT
        )
    """)

    try:
        conn.execute("ALTER TABLE base_conocimiento_salud ADD COLUMN imagen_url TEXT")
        conn.commit()
    except:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_y_clientes (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            celular TEXT,
            email TEXT,
            direccion_completa TEXT,
            ciudad_prov_pais TEXT,
            latitud REAL,
            longitud REAL
        )
    """)

    conn.commit()
    conn.close()
