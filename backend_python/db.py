import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",        # same as your MySQL
        password="root",        # empty if using XAMPP default
        database="helpreach_db"
    )
