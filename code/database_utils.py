import os
import time
import shutil
import sqlite3

from tkinter import messagebox

def create_tables_from_sql_files(db_file, sql_folder):
    if not os.path.exists(sql_folder):
        messagebox.showerror('File Not Found Error', f'The SQL folder "{sql_folder}" does not exist.')
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
        messagebox.showerror('File Not Found Error', f'The SQL folder "{sql_folder}" does not exist.')

    # Create missing tables from SQL files
    create_tables_from_sql_files(db_file, sql_folder)

    # Check again if all required tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]

    # Close the connection
    conn.close()

    # Return True if all required tables exist, otherwise False
    return set(required_tables).issubset(existing_tables)

def backupDatabase(db_file: str, backup_folder: str):
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    # Check for existing backup files and delete them
    existing_backups = [f for f in os.listdir(backup_folder) if f.endswith('.bak')]
    if existing_backups:
        for backup_file in existing_backups:
            os.remove(os.path.join(backup_folder, backup_file))
        # print(f"Existing backup files deleted successfully.")

    # Create new backup
    backup_file = os.path.join(backup_folder, f"{os.path.basename(db_file)}.bak")
    
    try:
        shutil.copy2(db_file, backup_file)
        # Get the current time
        current_time = time.time()
        # Set the modification time of the backup file
        os.utime(backup_file, (current_time, current_time))
        # print(f"Backup created successfully: {backup_file}")
    except IOError as e:
        messagebox.showerror('IOError', f'{e}')

def restoreDatabase(backup_file: str, db_file: str):
    try:
        shutil.move(backup_file, db_file)
        # Get the current time
        current_time = time.time()
        # Set the modification time of the restored database file
        os.utime(db_file, (current_time, current_time))
    except IOError as e:
        messagebox.showerror('IOError', f'{e}')


