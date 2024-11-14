import streamlit as st
from streamlit_option_menu import option_menu
from send_email import send_whatsapp_message
import re
#DB Imports
from db_colo import conn, cursor
import sqlite3

name = 'Complejo Deportivo Dos'
icono = r'assets\ico.ico'
horas = ['9:00','10:00','11:00']
canchas = ['Padel','Tenis','Futbol 5 Nro 1','Futbol 5 Nro 2','Futbol 7']

# funcion para validar el formato del email con expresiones regulares
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False
    


st.set_page_config(page_title = name, page_icon = icono, layout ='centered')

st.image('assets\complejodos.png')
st.title(name,anchor=False)
st.text('''         
                    Canchas de Fútbol 5-7, Tenis y Pádel ⚽️🎾
                    Snack Bar 🍻🥪
                    📲 3329535504
                    🏆 Copa Mundial “DOS” 23/24 🏆
                    📍Pérez Millán, prov. de Bs As.
        ''')

selected = option_menu(menu_title=None,options=['Reservar', 'Canchas', 'Detalles'], 
            icons=['calendar-date','building','clipboard-ninus'],
            orientation='horizontal')

if selected == 'Reservar':

    st.subheader('Reservar')
    c1,c2 = st.columns(2)

    nombre = c1.text_input('Nombre*')
    email = c2.text_input('Telefono*')
    fecha = c1.date_input('Fecha')
    hora = c2.selectbox('Hora',horas)
    canchas = c1.selectbox('Cancha', canchas)
    notas = c2.text_area('Notas')

    enviar = st.button('Reservar')
    if enviar:

        if nombre == '':
            st.warning('El nombre es obligatorio')
        elif email == '':
            st.warning('El teléfono es obligatorio')
        else:
            try:
                # Crear conexión y cursor dentro del bloque de inserción
                conn = sqlite3.connect('complejodos.db', check_same_thread=False)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO reservas (nombre, email, fecha, hora, canchas, notas)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (nombre, email, fecha, hora, canchas, notas))

                conn.commit()
                
                # Enviar mensaje de WhatsApp después de guardar la reserva
                send_whatsapp_message(
                    to_phone_number= email,  # Asegúrate de que 'email' contiene el número de teléfono
                    nombre=nombre,
                    fecha=fecha,
                    hora=hora,
                    pista=canchas
                )
                
                st.success('Pista reservada correctamente y mensaje de WhatsApp enviado')

            except sqlite3.Error as e:
                st.error(f"Error al guardar la reserva: {e}")
            except Exception as e:
                st.error(f"Error al enviar el mensaje de WhatsApp: {e}")
            finally:
                conn.close()