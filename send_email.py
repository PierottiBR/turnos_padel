from twilio.rest import Client
import streamlit as st

def send_whatsapp_message(
        to_phone_number,
        nombre,
        fecha,
        hora,
        pista
    ):
    # Credenciales de Twilio
    account_sid = st.secrets['account_sid']
    auth_token = st.secrets['auth_token']
    from_whatsapp_number = 'whatsapp:+5493329597242'  # Número de WhatsApp de Twilio proporcionado
    to_whatsapp_number = f'whatsapp:{to_phone_number}'

    client = Client(account_sid, auth_token)

    # Mensaje a enviar
    message_body = f'''
    Hola {nombre},
    La reserva ha sido guardada exitosamente.
    Fecha: {fecha}
    Hora: {hora}
    Pista: {pista}
    '''

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )
        st.success('Mensaje de WhatsApp enviado correctamente')
        return message.sid
    except Exception as e:
        st.error(f'Error al enviar el mensaje de WhatsApp: {e}')