import os
import psycopg
from dotenv import load_dotenv


load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}


def get_connection():
    try:
        connection = psycopg.connect(**DB_CONFIG)
        return connection

    except psycopg.Error as error:
        print(f"Database connection error: {error}")
        return None