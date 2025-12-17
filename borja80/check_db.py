import mysql.connector
from mysql.connector import Error

def check_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'urban_kicks'")
            result = cursor.fetchone()
            if result:
                print("Database 'urban_kicks' EXISTS.")
                connection.database = 'urban_kicks'
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print("Tables found:", [table[0] for table in tables])
                
                # Check columns in detalle_venta if it exists
                if ('detalle_venta',) in tables:
                     cursor.execute("DESCRIBE detalle_venta")
                     columns = cursor.fetchall()
                     print("\nColumns in detalle_venta:")
                     for col in columns:
                         print(col)
            else:
                print("Database 'urban_kicks' DOES NOT EXIST.")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    check_database()
