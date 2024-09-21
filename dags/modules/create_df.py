import requests
import pandas as pd
import datetime
from .create_connection import create_connection, API_KEY, REDSHIFT_SCHEMA

def weather_main_trad(weather):
    climas={
        'Thunderstorm': 'Tormenta eléctrica',
        'Drizzle': 'Llovizna',
        'Rain': 'Lluvia',
        'Snow': 'Nieve',
        'Clear': 'Despejado',
        'Clouds': 'Con nubes',
        'Smoke': 'Con humo'
    }
    traduccion = climas[f'{weather}']
    return traduccion

def create_df():

    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {REDSHIFT_SCHEMA}.localidades_corrientes")
        localidades = cur.fetchall()
    conn.close()
    appid = API_KEY
    units = 'metric'
    lang = 'es'
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

    for row in localidades:
        # Crear la URL con los valores de latitud y longitud
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={row[1]}&lon={row[2]}&lang={lang}&appid={appid}&units={units}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            ID = data['id']
            Name = row[0]
            Temperature = data['main']['temp']
            Feels_Like = data['main']['feels_like']
            Temp_Min = data['main']['temp_min']
            Temp_Max = data['main']['temp_max']
            Humidity = f"{data['main']['humidity']}%"
            Wind_Speed = f"{data['wind']['speed']} km/h"
            Weather = weather_main_trad(data['weather'][0]['main']) 
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