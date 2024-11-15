import sqlite3

conn = sqlite3.connect('complejodos.db')
cursor = conn.cursor()

#Creacion de tabla

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
    conn.commit()


    print("Tabla 'reservas' creada o verificada con éxito.")
except sqlite3.Error as e:
    print(f"Error al crear la tabla: {e}")

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deportes (
            deporte TEXT NOT NULL,
            canchas TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    ''')

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
    conn.commit()
    print("Valores predeterminados insertados correctamente en la tabla 'deportes'.")
except sqlite3.Error as e:
    print(f"Error al insertar datos: {e}")

finally:
    conn.close()  # Cerrar la conexión al final