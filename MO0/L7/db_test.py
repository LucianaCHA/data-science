import os
import mysql.connector

print("MYSQL_USER:", os.environ.get('MYSQL_USER')) 

try:
    conn = mysql.connector.connect(
        host='database',
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE']
    )
    print("Dale , dale, dale que se conectó la db")
except mysql.connector.Error as err:
    print(f"Puff , hay error: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
