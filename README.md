# DAG de Airflow para aviso del clima en Corrientes

## Descripción General

Este proyecto tiene como objetivo automatizar la extracción, transformación y carga (ETL) de datos climáticos mediante un **DAG en Apache Airflow**. El sistema se levanta utilizando **Docker Compose** y establece una conexión con una base de datos en **Amazon Redshift** para almacenar la información extraída. Además, dependiendo de los datos climáticos obtenidos, se envía un correo electrónico informando sobre el clima en un departamento específico de la provincia de Corrientes.

## Componentes Principales

1. **Docker Compose**: Se utiliza para orquestar los contenedores necesarios, incluyendo Apache Airflow.
2. **Apache Airflow**: Ejecuta el DAG diario que realiza la operación ETL.
3. **Amazon Redshift**: Base de datos en la nube donde se almacenan los datos climáticos.
4. **API pública**: Fuente de datos meteorológicos extraidos de la API de <a href="https://openweathermap.org/" target="_blank">OpenWeather</a>.
5. **Sistema de correo**: Envío de notificaciones por correo electrónico basado en los valores climáticos.

## Flujos del Proyecto

### 1. Configuración Inicial
- **Docker Compose**: El `docker-compose.yaml` se encarga de levantar los servicios de Airflow. Incluye los contenedores necesarios para el Scheduler, Web Server, Worker y PostgreSQL como backend de Airflow.
- **Configuración de Redshift**: El DAG establece la conexión a Redshift utilizando las credenciales proporcionadas en las variables guardadas dentro de la metabase de Airflow.

### 2. Creación de la Tabla en Redshift
- Primero se debera crear una tabla en la base de datos Redshift mediante una consulta SQL que contenga los siguientes campos: 
    1. Nombre de los departamentos de la provincia que seleccionemos (en este caso Corrientes).
    2. Latitud de la capital de estos departamentos.
    3. Longitud de la capital de estos departamentos.
    
Con esta tabla podremos recorrer la API obteniendo asi los datos climaticos de los distintos departamentos de la provincia seleccionada. 
- Al iniciarse el DAG, primero crea una tabla en la base de datos Redshift con la estructura adecuada para almacenar los datos climáticos que se extraerán de la API.

### 3. Extracción de Datos de la API Pública
- Utilizando una función previamente creada, el DAG, mediante un **PythonOperator** hace una solicitud HTTP a una API pública para obtener datos meteorológicos. Estos datos incluyen sensación térmica, temperaturas máximas y mínimas, descripción del clima, humedad, entre otros.

### 4. Transformación de los Datos
- Los datos crudos obtenidos de la API pasan por un proceso de transformación. Esto incluye limpieza de datos y el filtrado de la información relevante.
- Los datos transformados se cargan en un **DataFrame de Pandas** para su posterior inserción en la base de datos.

### 5. Carga de los Datos en Redshift
- Una vez transformados los datos, se insertan en la tabla previamente creada en la base de datos Redshift utilizando una función hecha en Python mediante un **PythonOperator**.

### 6. Selección de Datos de la Tabla
- Luego de la carga, se realiza una consulta a la tabla en Redshift para obtener los datos relevantes del clima de un departamento específico de la provincia de Corrientes que seleccionemos (lo hacemos desde `dags/modules/get_data.py`).

### 7. Envío de Correo de Notificación
- Dependiendo de los valores climáticos obtenidos se envía una notificación por correo electrónico informando del clima en el departamento elegido.

## Estructura de Archivos

- `docker-compose.yaml`: Define los servicios necesarios para ejecutar Apache Airflow y la base de datos.
- `dags/`: Contiene el archivo dag.py y los modulos a utilizar para ejecutar las tareas previamente descriptas.
    - `dag.py`: Archivo que define el flujo de trabajo y las configuraciones del mismo.
    - `modules/`: Carpeta contenedora de los archivos .py con las funciones a utilizar.
        - `__init__.py`
        - `create_connection.py`
        - `create_df.py`
        - `create_table.py`
        - `get_data.py`
        - `insert_data.py`
        - `send_email.py`
  
## Variables de Entorno

Para establecer las conexiones y credenciales necesarias, se deben configurar las siguientes variables de entorno en el archivo `.env`:

- `AIRFLOW_UID`: ID de usuario que ejecuta los servicios de Airflow, generalmente utilizado para definir permisos de acceso a los contenedores Docker.
- `AIRFLOW__SMTP__SMTP_HOST`: Host o servidor SMTP que Airflow utilizará para enviar correos electrónicos.
- `AIRFLOW__SMTP__SMTP_PORT`: Puerto del servidor SMTP para el envío de correos electrónicos.
- `AIRFLOW__SMTP__SMTP_STARTTLS`: Configura si el servidor SMTP debe usar el protocolo STARTTLS para asegurar las comunicaciones.
- `AIRFLOW__SMTP__SMTP_SSL`: Indica si el servidor SMTP debe usar SSL (Secure Sockets Layer) para cifrar la conexión.
- `AIRFLOW__SMTP__SMTP_USER`: Nombre de usuario del servidor SMTP utilizado para autenticar el envío de correos.
- `AIRFLOW__SMTP__SMTP_PASSWORD`: Contraseña del servidor SMTP para la autenticación en el envío de correos.
- `AIRFLOW__SMTP__SMTP_MAIL_FROM`: Dirección de correo desde la cual Airflow enviará los correos electrónicos.
- `AIRFLOW_VAR_EMAIL`: Variable personalizada de Airflow que almacena la dirección de correo del remitente.
- `AIRFLOW_VAR_EMAIL_PASSWORD`: Variable personalizada de Airflow que contiene la contraseña para autenticar el correo del remitente.
- `AIRFLOW_VAR_TO_ADDRESS`: Dirección de correo del destinatario a la cual Airflow enviará los correos.
- `dbname`: Nombre de la base de datos en Redshift que se utilizará para las conexiones.
- `host`: Dirección del host de la base de datos Redshift.
- `user`: Usuario utilizado para autenticar la conexión a la base de datos en Redshift.
- `pwd`: Contraseña utilizada para autenticar la conexión a la base de datos en Redshift.
- `port`: Puerto en el que está escuchando la base de datos Redshift para las conexiones.
- `REDSHIFT_SCHEMA`: Esquema en la base de datos Redshift donde se realizarán las operaciones.
- `API_KEY`: Clave de acceso a una API, que permite la autenticación y autorización para consumir sus servicios.
- `email`: Variable personalizada de Airflow que almacena la dirección de correo del remitente.

## Ejecución

### 1. Levantar los Servicios
Primero inicializamos el entorno de Airflow y la base de datos que utilizara, lo hacemos abriendo una terminal dentro de la carpeta que contiene el archivo docker-compose mediante:

```bash
docker compose up airflow-init
```

Una vez finalizado, podemos iniciar todos los servicios definidos dentro del archivo docker-compose mediante:

```bash
docker compose up
```

### 2. Configurar el DAG en Airflow
El DAG se encuentra en el directorio /dags y se ejecutará diariamente a las 0:00 PM (hora de Argentina). Se puede monitorear desde la interfaz web de Airflow.

### 3. Verificación de la Carga en Redshift
Después de la ejecución del DAG, los datos estarán almacenados en la tabla en Redshift, que se puede consultar usando SQL estándar.

### 4. Notificación por Correo
El DAG envía un correo en base a la temperatura de la hora en que se ejecute. El contenido del correo también estara personalizado de acuerdo a los datos obtenidos desde la API para un departamento especifico seleccionado.

## Detener los Servicios
Para detener los servicios de Docker, ejecuta el siguiente comando:

```bash
docker-compose down
```

Esto detendrá y eliminará los contenedores, pero mantendrá los volúmenes de datos y las redes asociadas.