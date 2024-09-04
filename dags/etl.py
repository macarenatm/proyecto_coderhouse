import requests
import pandas as pd
import datetime
import psycopg2
from psycopg2.extras import execute_values
from airflow.models import Variable

def create_connection():
    try:
        dbname = Variable.get('dbname')
        host = Variable.get('host')
        user = Variable.get('user')
        pwd = Variable.get('pwd')
        port = Variable.get('port')

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

def create_table():
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS macarenataie_coderhouse.clima_corrientes(
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

def create_df():
    appid = '929e7a3a1b3cafec69b3c08796e6dae7'
    units = 'metric'
    localidades_corrientes = {
        "nombre": [
            "Corrientes", "Bella Vista", "Berón de Astrada", "Concepción", "Cururú Cuatiá",
            "Empedrado", "Esquina", "General Alvear", "San Luis del Palmar", "San Martin",
            "San Miguel", "San Roque", "Santo Tomé", "Sauce", "Tapebicuá",
            "General Paz", "Goya", "Itatí", "Ituzaingó", "Lavalle",
            "Mburucuyá", "Mercedes", "Monte Caseros", "Paso de los Libres", "San Cosme"],
        "lat": [
            -27.5337, -28.5069, -27.5514, -28.3945, -29.7907, 
            -27.9529, -30.0184, -29.0896, -27.5124, -29.1782,
            -27.9946, -28.5748, -28.5526, -30.0862, -29.5069,
            -27.7505, -29.1440, -27.2725, -27.5883, -29.0286,
            -28.0483, -29.1852, -30.2529, -29.7136, -27.3716],
        "lon": [
            -58.9023, -59.0450, -57.5302, -57.8895, -58.0559, 
            -58.8063, -59.5310, -56.5442, -58.5620, -56.6383,
            -57.5922, -58.7072, -56.0438, -58.7880, -56.9751,
            -57.6201, -59.2651, -58.2429, -56.6907, -59.1831,
            -58.2257, -58.0714, -57.6379, -57.0868, -58.5115]
    }
    clima = {
            'id': [],
            'name': [],
            'temperature': [],
            'feels_like': [],
            'temp_min': [],
            'temp_max': [],
            'humidity': [],
            'wind_speed': [],
            'weather': [],
            'weather_desc': [],
            'dt' : []
    }

    for nombre, lat, lon in zip(localidades_corrientes['nombre'], localidades_corrientes['lat'], localidades_corrientes['lon']):
        # Crear la URL con los valores de latitud y longitud
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}&units={units}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            ID = data['id']
            Name = nombre
            Temperature = data['main']['temp']
            Feels_Like = data['main']['feels_like']
            Temp_Min = data['main']['temp_min']
            Temp_Max = data['main']['temp_max']
            Humidity = f"{data['main']['humidity']}%"
            Wind_Speed = f"{data['wind']['speed']} km/h"
            Weather = data['weather'][0]['main']
            Weather_Desc = data['weather'][0]['description']
            DT = datetime.datetime.fromtimestamp(data['dt'])

            clima['id'].append(ID)
            clima['name'].append(Name)
            clima['temperature'].append(Temperature)
            clima['feels_like'].append(Feels_Like)
            clima['temp_min'].append(Temp_Min)
            clima['temp_max'].append(Temp_Max)
            clima['humidity'].append(Humidity)
            clima['wind_speed'].append(Wind_Speed)
            clima['weather'].append(Weather)
            clima['weather_desc'].append(Weather_Desc)
            clima['dt'].append(DT)

        elif response.status_code == 404:
            return print('Recurso no encontrado')

        else:
            return print(f'Error: Codigo de estado {response.status_code}')

    df = pd.DataFrame(clima)
    return df

def insert_data():
    conn = create_connection()
    df = create_df()
    with conn.cursor() as cur:
        try:
            execute_values(
                cur, 'INSERT INTO macarenataie_coderhouse.clima_corrientes VALUES %s',
                [tuple(row) for row in df.values],
                page_size=len(df)
            )
            conn.commit()
        except Exception as e:
            print(f'No se pueden ingresar datos. Error {e}')

    conn.close()