# introspect.py - foundation, connects to psycopg2 and introspects the database to get table & column info

# imports

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # load env variables from .env file

# variables

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# connect to DB func
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return conn

    except Exception as e:
        print(f"error while connecting to the database: {e}")
        return None

# get_tables func to get tables of a schema
def get_tables(conn, schema='public'):
    # check if conn is none
    if conn is None:
        raise ValueError("Connection object is None. Please provide a valid connection.")

    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_type = 'BASE TABLE';", (schema,))

    tuple_list = cursor.fetchall() # it's a tuple list, but we need it in a string list format
    cursor.close() # close cursor, done with query
    str_list = [row[0] for row in tuple_list] # convert tuple list to string list
    return str_list

# get_columns func to get columns of a table
def get_columns(conn, table_name, schema='public'):
    # check conn
    if conn is None:
        raise ValueError("Connection object is None. Please provide a valid connection.")

    cursor = conn.cursor()
    cursor.execute("SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = %s AND table_schema = %s;", (table_name, schema))
    rows = cursor.fetchall()
    result = [
        {"name": row[0], "type": row[1], "nullable": row[2], "default": row[3]} for row in rows
    ]
    cursor.close()

    return result