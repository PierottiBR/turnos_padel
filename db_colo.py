import sqlite3

conn = sqlite3.connect('complejodos.db')
cursor = conn.cursor()

#Creacion de tabla

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            canchas TEXT NOT NULL,
            notas TEXT
        )
    ''')
    conn.commit()
    print("Tabla 'reservas' creada o verificada con éxito.")
except sqlite3.Error as e:
    print(f"Error al crear la tabla: {e}")
finally:
    conn.close()  # Cerrar la conexión al final