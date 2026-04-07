import mariadb
import os
from dotenv import load_dotenv

# Esto busca el archivo .env y carga los datos
load_dotenv()

def get_db_connection():
    try:
        # Aquí usamos os.getenv para leer del archivo .env
        conn = mariadb.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return None