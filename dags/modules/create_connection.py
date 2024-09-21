import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def create_connection():
    try:
        
        dbname = os.getenv("dbname")
        host = os.getenv("host")
        user = os.getenv("user")
        pwd = os.getenv("pwd")
        port = os.getenv("port")

        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=pwd,
            host=host,
            port=port
        )

        return conn

    except Exception as e:
        return print(f"No se puede establecer la conexion. Error {e}")

REDSHIFT_SCHEMA = os.getenv("REDSHIFT_SCHEMA")
API_KEY = os.getenv("API_KEY")