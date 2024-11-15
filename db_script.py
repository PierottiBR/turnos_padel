import sqlite3
import os

# Ruta del archivo de la base de datos
db_path = 'complejodos.db'

# Verificar si el archivo ya existe y si es accesible
if os.path.exists(db_path):
    print(f"La base de datos '{db_path}' ya existe.")
else:
    print(f"La base de datos '{db_path}' no existe. Se creará.")

# Usamos un bloque 'with' para manejar la conexión y cerrar automáticamente
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Creación de la tabla 'reservas'
    try:
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                cancha TEXT NOT NULL,
                deporte TEXT NOT NULL,
                notas TEXT
            )
        ''')
        print("Tabla 'reservas' creada o ya existe.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'reservas': {e}")

    # Creación de la tabla 'deportes'
    try:
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS deportes (
                deporte TEXT NOT NULL,
                canchas TEXT NOT NULL,
                hora TEXT NOT NULL
            )
        ''')
        print("Tabla 'deportes' creada o ya existe.")
        
        # Datos predeterminados para insertar
        deportes_data = [
            ('padel', 'padel N1', '13:00'),
            ('padel', 'padel N1', '14:30'),
            ('padel', 'padel N1', '16:00'),
            ('padel', 'padel N1', '17:30'),
            ('padel', 'padel N1', '19:00'),
            ('padel', 'padel N1', '20:30'),
            ('padel', 'padel N1', '22:00'),
            ('padel', 'padel N1', '23:30'),
            ('padel', 'padel N1', '01:00'),
            ('padel', 'padel N2', '13:00'),
            ('padel', 'padel N2', '14:30'),
            ('padel', 'padel N2', '16:00'),
            ('padel', 'padel N2', '17:30'),
            ('padel', 'padel N2', '19:00'),
            ('padel', 'padel N2', '20:30'),
            ('padel', 'padel N2', '22:00'),
            ('padel', 'padel N2', '23:30'),
            ('padel', 'padel N2', '01:00'),
            ('futbol', 'futbol n5 1', '14:00'),
            ('futbol', 'futbol n5 1', '15:00'),
            ('futbol', 'futbol n5 1', '16:00'),
            ('futbol', 'futbol n5 2', '14:00'),
            ('futbol', 'futbol n5 2', '15:00'),
            ('futbol', 'futbol n5 2', '16:00'),
            ('futbol', 'futbol n7', '14:00'),
            ('futbol', 'futbol n7', '15:00'),
            ('futbol', 'futbol n7', '16:00'),
            ('tenis', 'tenis', '14:00'),
            ('tenis', 'tenis', '15:30'),
            ('tenis', 'tenis', '17:00')
        ]
        
        cursor.executemany(''' 
            INSERT INTO deportes (deporte, canchas, hora) 
            VALUES (?, ?, ?)
        ''', deportes_data)
        print("Valores predeterminados insertados correctamente en la tabla 'deportes'.")
        
    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'deportes' o insertar los datos: {e}")

# Verificar que las tablas se hayan creado correctamente
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tablas en la base de datos:", tables)