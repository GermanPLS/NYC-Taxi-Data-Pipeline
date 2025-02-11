# Ingesting NY Taxi Data to Postgres

Este proyecto se basa en el Ejercicio Práctico  °1 del **[Data Engineering Zoomcamp](https://datatalks.club/blog/guide-to-free-online-courses-at-datatalks-club.html#data-engineering-zoomcamp)**
de DataTalks.Club.

Dataset: http://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Dictionary: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

 🚀 Tecnologías utilizadas : 

    - Python (para el procesamiento de datos)

    - PostgreSQL (base de datos relacional para almacenar los datos)
 
    - pgAdmin (herramienta web para administrar PostgreSQL)
 
    - Docker & Docker Compose (para la gestión de contenedores)
 
    - Jupyter Notebook (para desarrollar y probar el código de ingestión y transformación de datos)
 
    - Git (para control de versiones)

Clonar el repositorio

    git clone https://github.com/tu_usuario/NYC-Taxi-Data-Pipeline.git
    cd NYC-Taxi-Data-Pipeline



# Paso a Paso 
📂 Estructura del proyecto

## 1️⃣ Verificación e instalación de herramientas

    NYC-Taxi-Data-Pipeline/
    │── docker-compose.yml   # Configuración de los contenedores
    │── requirements.txt     # Dependencias de Python
    │── notebooks/           # Jupyter Notebooks para el procesamiento de datos
    │── scripts/             # Scripts Python para la extracción y carga de datos
    │── data/                # Archivos de datos descargados
    │── README.md            # Documentación del proyecto

  Ejecuta los siguientes comandos en la terminal  para verificar si ya estan instaladas, sino hay que installarlas:

   - Verificar si Git está instalado
   
         git --version

   - Verificar si Python está instalado
     
         python --version
     
   - Verificar si Docker está instalado y en ejecución
     
         docker --version


## 2️⃣ Configuración del entorno del proyecto

  Creamos la estructura del proyecto (Carpetas) en mi disco, para un mejor rendimiento:

    mkdir proyectos
    cd proyectos
    mkdir nyc_taxi_pipeline
    cd nyc_taxi_pipeline
    mkdir notebooks scripts data

Iniciamos Git:

    git init

## 3️⃣ Configurar Docker con PostgreSQL y pgAdmin

   Creamos un archivo docker-compose.yml dentro de nyc_taxi_pipeline para levantar PostgreSQL y pgAdmin:


    version: "3.8"

    services:
      postgres:
        image: postgres:latest
        container_name: postgres_nyc
        restart: always
        environment:
          POSTGRES_USER: admin
          POSTGRES_PASSWORD: admin
          POSTGRES_DB: nyc_taxi
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data
    
      pgadmin:
        image: dpage/pgadmin4
        container_name: pgadmin_nyc
        restart: always
        environment:
          PGADMIN_DEFAULT_EMAIL: admin@admin.com
          PGADMIN_DEFAULT_PASSWORD: admin
        ports:
          - "5050:80"
    
    volumes:
      postgres_data:

Ejecutamos el contenedor:

    docker-compose up -d


Creamos el archivo requirements.txt :

    pandas
    numpy
    sqlalchemy
    psycopg2-binary
    jupyter
    requests
    pyarrow

## 4️⃣ Creación del entorno virtual de Python

   Dentro de nyc_taxi_pipeline, creamos el entorno virtual y activamos:


       python3 -m venv venv
       source venv/bin/activate
  
   Instalamos las librerías necesarias:  

      # pip install pandas pyarrow sqlalchemy psycopg2-binary notebook
        pip install -r requirements.txt
        
## 5️⃣ Desarrollo del script en Jupyter Notebook

    jupyter notebook


 Se nos abre una pagina web: http://localhost:8888/ ; debemos invresar en la carpeta `env` :

     New --> Python 3 ( nuevo notebook)

![[imagen1](./imagenes/jupyter_notebook.png)](https://github.com/GermanPLS/NYC-Taxi-Data-Pipeline/blob/79e38102c8cddc7c3641fd0bd9f1b324d3eb64f1/imagenes/jupyter_notebook.png)
     
en el notebook escribimos el código para la extracción, transformación y carga en PostgreSQL:

```sh
    import pandas as pd
    from sqlalchemy import create_engine
    
    # Conexión a PostgreSQL
    engine = create_engine("postgresql://admin:admin@localhost:5432/nyc_taxi")
    
    # Descarga del archivo
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-11.parquet"
    df = pd.read_parquet(url)
    
    # Transformaciones necesarias
    df = df.rename(columns=str.lower)  # Ejemplo de transformación
    
    # Carga en la base de datos
    df.to_sql("yellow_taxi_data", engine, if_exists="replace", index=False)
    
```


## 6️⃣ Acceso a pgAdmin
    Abre un navegador y accede a `http://localhost:5050` para gestionar la base de datos visualmente.     

    Para la configuracion: 

                              1) Registra un servidor en pgAdmin
                                  Haz clic derecho sobre "Servers" (en el panel izquierdo).
                                  Elige la opción "Register" → "Server...".
                              
                              
                               2) Configura el servidor
                              
                                  Una vez que selecciones "Server", aparecerá una ventana para configurar la conexión. Aquí debes ingresar los siguientes datos:
                              
                                  Pestaña "General":
                                      Name: Escribe un nombre para la conexión.
                                  
                                  
                                  Pestaña "Connection":
                              
                                      Host name/address: localhost
                                      Port: 5432 (puerto predeterminado de PostgreSQL).
                                      Maintenance database: nyc_taxi (el nombre de tu base de datos).
                                      Username: admin (o el nombre de usuario configurado).
                                      Password: admin (o la contraseña que configuraste).
                                      
                                      Haz clic en Save para guardar la configuración.

                                 3) Ver las tablas en pgAdmin:
                                   Ahora deberías ver tu servidor en Servers (en el panel izquierdo). Expándelo y navega hacia:

                                                 Databases → nyc_taxi → Schemas → public → Tables.



                                  4)  Ver los datos de una tabla
                                      Para ver los datos, haz clic derecho sobre la tabla que quieres consultar y selecciona View/Edit Data → All Rows.

   ![[imagen2](./imagenes/pgadmin.png)](https://github.com/GermanPLS/NYC-Taxi-Data-Pipeline/blob/399700ee08d89984397dd6568dda4728e6139d55/imagenes/pgadmin.png)                                 
![image](https://github.com/user-attachments/assets/75144a93-5c22-4386-8b72-f953a7ac5a25)

## 7️⃣ Automatización con un script en Python
Creamos un script en la carpeta scripts/:  `extract_transform_load.py`

    import pandas as pd
    import pyarrow
    import fastparquet
    from sqlalchemy import create_engine
    from sqlalchemy.exc import SQLAlchemyError
    
    def main():
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-11.parquet"
        db_url = "postgresql://admin:admin@localhost:5432/nyc_taxi"

    try:
        print("Iniciando ejecución del script...")
        
        print("Descargando el archivo Parquet...")
        # Cargar los datos desde la URL
        df = pd.read_parquet(url)

        print(f"Archivo descargado y cargado. Número de filas: {len(df)}")

        if df.empty:
            print("El DataFrame está vacío. No se insertarán datos.")
            return

        print("Conectando a la base de datos...")
        # Crear conexión a la base de datos
        engine = create_engine(db_url)
        with engine.connect() as conn:
            print("Insertando datos en la base de datos...")
            df.to_sql("yellow_taxi_data", conn, if_exists="replace", index=False)

        print("Pipeline completado")

    except pd.errors.EmptyDataError:
        print("Error: El archivo Parquet está vacío o no es válido.")
    except SQLAlchemyError as e:
        print(f"Error de base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    if __name__ == "__main__":
    main()


Ejecutamos el script:

    python extract_transform_load.py





    
