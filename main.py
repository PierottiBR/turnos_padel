import streamlit as st
from streamlit_option_menu import option_menu
from send_email import send_whatsapp_message
import re
# DB Imports
import sqlite3

name = 'Complejo Deportivo Dos'
icono = r'assets\ico.ico'

# Conexión a la base de datos
conn = sqlite3.connect('complejodos.db', check_same_thread=False)
cursor = conn.cursor()

# Obtener los deportes disponibles desde la base de datos
cursor.execute("SELECT DISTINCT deporte FROM deportes")
deportes = [row[0] for row in cursor.fetchall()]

# Cerrar la conexión cuando ya no sea necesaria
conn.close()

# Función para validar el formato del email con expresiones regulares
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

# Guardar el estado en session_state
if 'deporte_seleccionado' not in st.session_state:
    st.session_state.deporte_seleccionado = None
if 'canchas' not in st.session_state:
    st.session_state.canchas = []

st.set_page_config(page_title=name, page_icon=icono, layout='centered')

st.image('assets\complejodos.png')
st.title(name, anchor=False)
st.text('''         
                    Canchas de Fútbol 5-7, Tenis y Pádel ⚽️🎾
                    Snack Bar 🍻🥪
                    📲 3329535504
                    🏆 Copa Mundial “DOS” 23/24 🏆
                    📍Pérez Millán, prov. de Bs As.
        ''')

selected = option_menu(menu_title=None, options=['Reservar', 'Canchas', 'Detalles'], 
            icons=['calendar-date', 'building', 'clipboard-ninus'],
            orientation='horizontal')

if selected == 'Reservar':
    st.subheader('Reservar')

    # Crear un contenedor de botones para los deportes
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button( 'Padel ',icon='🎾'):
            st.session_state.deporte_seleccionado = deportes[0]
    with col2:
        if st.button('Futbol ', icon='⚽️'):
            st.session_state.deporte_seleccionado = deportes[1]
    with col3:
        if st.button('Tenis ', icon='🎾'):
            st.session_state.deporte_seleccionado = deportes[2]

    if st.session_state.deporte_seleccionado:
        st.write(f"Reservar turno para **{st.session_state.deporte_seleccionado}**")

        # Conectar a la base de datos para obtener las canchas disponibles para el deporte seleccionado
        conn = sqlite3.connect('complejodos.db', check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT canchas FROM deportes WHERE deporte = ?
        """, (st.session_state.deporte_seleccionado,))
        st.session_state.canchas = [row[0] for row in cursor.fetchall()]
        conn.close()

        if st.session_state.canchas:
            c1, c2 = st.columns(2)

            nombre = c1.text_input('Nombre*')
            telefono = c2.text_input('Teléfono*')
            fecha = c1.date_input('Fecha')
            canchas = c1.selectbox('Cancha', st.session_state.canchas)
            notas = c2.text_area('Notas')

            # Conectar nuevamente a la base de datos para obtener las horas disponibles para el deporte y cancha seleccionados
            conn = sqlite3.connect('complejodos.db', check_same_thread=False)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT hora FROM deportes WHERE deporte = ? AND canchas = ?
            """, (st.session_state.deporte_seleccionado, canchas))
            horas_disponibles = [row[0] for row in cursor.fetchall()]

            # Consultar las horas ya reservadas para la fecha seleccionada
            cursor.execute("""
                SELECT hora FROM reservas WHERE fecha = ?
            """, (str(fecha),))
            horas_reservadas = [row[0] for row in cursor.fetchall()]

            # Filtrar las horas disponibles eliminando las horas reservadas
            horas_disponibles = [hora for hora in horas_disponibles if hora not in horas_reservadas]

            conn.close()

            # Mostrar la hora solo si hay horas disponibles
            if horas_disponibles:
                hora = c2.selectbox('Hora', horas_disponibles)
            else:
                st.warning("No hay horas disponibles para esta fecha. Por favor, elige otra fecha.")

            enviar = st.button('Reservar')
            if enviar:

                if nombre == '':
                    st.warning('El nombre es obligatorio')
                elif telefono == '':
                    st.warning('El teléfono es obligatorio')
                else:
                    try:
                        # Crear conexión y cursor dentro del bloque de inserción
                        conn = sqlite3.connect('complejodos.db', check_same_thread=False)
                        cursor = conn.cursor()

                        # Insertar la reserva en la base de datos
                        cursor.execute('''
                            INSERT INTO reservas (nombre, telefono, fecha, notas, cancha, hora, deporte)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (nombre, telefono, str(fecha), notas, canchas, hora, st.session_state.deporte_seleccionado))

                        conn.commit()

                        # Enviar mensaje de WhatsApp después de guardar la reserva
                        send_whatsapp_message(
                            to_phone_number=telefono,
                            nombre=nombre,
                            fecha=fecha,
                            hora=hora,
                            pista=canchas
                        )

                        st.success('Pista reservada correctamente y mensaje de WhatsApp enviado')
                        st.write(f"**Detalles de la reserva**")
                        st.write(f"**Nombre:** {nombre}")
                        st.write(f"**Teléfono:** {telefono}")
                        st.write(f"**Fecha:** {fecha}")
                        st.write(f"**Hora:** {hora}")
                        st.write(f"**Cancha:** {canchas}")
                        st.write(f"**Notas:** {notas}")
                    except sqlite3.Error as e:
                        st.error(f"Error al guardar la reserva: {e}")
                    except Exception as e:
                        st.error(f"Error al enviar el mensaje de WhatsApp: {e}")
                    finally:
                        conn.close()
        else:
            st.warning("No hay canchas disponibles para este deporte.")
