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
        df = pd.read_parquet(url)

        print(f"Archivo descargado y cargado. Número de filas: {len(df)}")

        if df.empty:
            print("El DataFrame está vacío. No se insertarán datos.")
            return

        print("Conectando a la base de datos...")
        engine = create_engine(db_url)

        print("Insertando datos en la base de datos...")
        df.to_sql("yellow_taxi_data", engine, if_exists="replace", index=False)

        print("Pipeline completado")

    except pd.errors.EmptyDataError:
        print("Error: El archivo Parquet está vacío o no es válido.")
    except SQLAlchemyError as e:
        print(f"Error de base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
