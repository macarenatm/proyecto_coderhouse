from psycopg2.extras import execute_values
from .create_connection import create_connection, REDSHIFT_SCHEMA
from .create_df import create_df

def insert_data():
    conn = create_connection()
    df = create_df()
    with conn.cursor() as cur:
        try:
            execute_values(
                cur, f'INSERT INTO {REDSHIFT_SCHEMA}.clima_corrientes VALUES %s',
                [tuple(row) for row in df.values],
                page_size=len(df)
            )
            conn.commit()
        except Exception as e:
            print(f'No se pueden ingresar datos. Error {e}')

    conn.close()