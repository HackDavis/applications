import psycopg2
import psycopg2.pool
import os
pool = None
def get_connection():
    global pool
    if not pool:
        pool = psycopg2.pool.ThreadedConnectionPool(1, 4, dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), host=os.getenv("DB_HOSTNAME"), password=os.getenv("DB_PASSWORD"))
    """returns the current connection to the database. If none exists, create one"""
    return pool.getconn()

def return_connection(conn):
    global pool
    if not pool:
        raise Exception("connection not initialized")
    pool.putconn(conn)

def execute_query(query, vars=None):
    """returns a cursor from the executed query"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, vars)

        conn.commit()
    
    except Exception as e:
        print(e)
    finally:
        return_connection(conn)
    return cursor
