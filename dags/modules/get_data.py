from .create_connection import create_connection, REDSHIFT_SCHEMA
from datetime import datetime

def get_data(**kwargs):

    departamento = 'Corrientes'

    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute(f"""SELECT departamento, temperatura, sensacion_termica, clima, humedad, descripcion, DATE(ultima_actualizacion) as ult_act
                        FROM {REDSHIFT_SCHEMA}.clima_corrientes
                        WHERE departamento = '{departamento}' AND ult_act = '{datetime.now().date()}'
                        ORDER BY ultima_actualizacion DESC;
                        """)
        data = cur.fetchall()
    conn.close()

    print(data)

    kwargs['ti'].xcom_push(key='data', value=data)