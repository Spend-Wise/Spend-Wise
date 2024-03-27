import os
import sqlite3

def create_tables_from_sql_files(db_file, sql_folder):
    if not os.path.exists(sql_folder):
        raise FileNotFoundError(f"The SQL folder '{sql_folder}' does not exist.")
    else:
        if not os.path.exists(db_file):
            # If database doesn't exist, create it
            conn = sqlite3.connect(db_file)
            conn.close()

    # Check if SQL folder exists

    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get list of SQL files in the folder
    sql_files = [file for file in os.listdir(sql_folder) if file.endswith(".sql")]

    # Iterate through SQL files and create tables if missing
    for sql_file in sql_files:
        table_name = os.path.splitext(sql_file)[0]
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        existing_table = cursor.fetchone()
        if not existing_table:
            # Table doesn't exist, read SQL file and create table
            sql_file_path = os.path.join(sql_folder, sql_file)
            with open(sql_file_path, 'r') as f:
                table_query = f.read()
                cursor.execute(table_query)
                # print(f"Table '{table_name}' created.")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

def ensure_database_structure(db_file :str, sql_folder :str, required_tables: tuple):
    # Check if database exists
    if not os.path.exists(db_file):
        # If database doesn't exist, create it
        conn = sqlite3.connect(db_file)
        conn.close()
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]

    # Check if all required tables exist
    if set(required_tables).issubset(existing_tables):
        # All required tables exist, close the connection and return True
        conn.close()
        return True

    # Check if SQL folder exists
    if not os.path.exists(sql_folder):
        raise FileNotFoundError(f"The SQL folder '{sql_folder}' does not exist.")

    # Create missing tables from SQL files
    create_tables_from_sql_files(db_file, sql_folder)

    # Check again if all required tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]

    # Close the connection
    conn.close()

    # Return True if all required tables exist, otherwise False
    return set(required_tables).issubset(existing_tables)


