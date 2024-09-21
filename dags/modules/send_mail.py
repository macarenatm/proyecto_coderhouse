import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(**context):
    from_address = context["var"]["value"].get("email")
    password = context["var"]["value"].get("email_password")
    to_address = context["var"]["value"].get("to_address")

    # Traemos la información que utilizaremos en el correo.
    data = context['ti'].xcom_pull(task_ids='get_data', key='data')

    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = to_address

    # Cremos una condicion para elegir el asunto y el contenido del mail.
    if data[0][1] >= 20:
        message['Subject'] = f'Información del tiempo hoy en {data[0][0]}'
        html_content = f"""
            <html>
                <body>
                    <h2>En {data[0][0]} el día de hoy estará caluroso.</h2>
                    <h3>Temperatura: {data[0][1]}°C.</h3>
                    <ul>
                        <li>Sensación térmica: {data[0][2]}°C.</li>
                        <li>Humedad: {data[0][4]}.</li>
                        <li>Clima: {data[0][3]}.</li>
                        <li>Descripción: {data[0][5]}.</li>
                        <li>Recomendación: <strong>Usar protector solar.</strong></li>
                    </ul>
                    <h3>Que tengas un lindo día!</h3>
                </body>
            </html>
        """
    else:
        message['Subject'] = f'Información del tiempo hoy en {data[0][0]}'
        html_content = f"""
            <html>
                <body>
                    <h2>En {data[0][0]} el día de hoy estará fresco.</h2>
                    <h3>Temperatura: {data[0][1]}°C.</h3>
                    <ul>
                        <li>Sensación térmica: {data[0][2]}°C.</li>
                        <li>Humedad: {data[0][4]}.</li>
                        <li>Clima: {data[0][3]}.</li>
                        <li>Descripción: {data[0][5]}.</li>
                        <li>Recomendación: <strong>Usar protector solar y llevar abrigo.</strong></li>
                    </ul>
                    <h3>Que tengas un lindo día!</h3>
                </body>
            </html>
        """
    
    message.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        text = message.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Correo enviado correctamente!!")
    except Exception as e:
        print(f"Hubo un problema: {str(e)}")
    