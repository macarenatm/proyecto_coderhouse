from .create_connection import create_connection, REDSHIFT_SCHEMA

def create_table():
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {REDSHIFT_SCHEMA}.clima_corrientes(
                ID INT NOT NULL,
                Departamento VARCHAR(100),
                Temperatura FLOAT,
                Sensacion_Termica FLOAT,
                Temperatura_Min FLOAT,
                Temperatura_Max FLOAT,
                Humedad VARCHAR(5),
                Velocidad_Viento VARCHAR(20),
                Clima VARCHAR(100),
                Descripcion VARCHAR(100),
                Ultima_Actualizacion VARCHAR(100) NOT NULL,
                CONSTRAINT PK_clima_corrientes PRIMARY KEY (ID, Ultima_Actualizacion));
            """)
        conn.commit()
    conn.close()