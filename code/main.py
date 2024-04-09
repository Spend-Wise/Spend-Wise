import os
import atexit
import keyboard
import subprocess

import tkinter as tk

from dotenv import load_dotenv
from registerPage import RegisterPage

from database_utils import ensure_database_structure, backupDatabase

load_dotenv()

DATABASE = os.environ.get("DATABASE")

SQL_FOLDER = os.environ.get("SQL_FOLDER")
BACKUP_FOLDER = os.environ.get("DATABASE_BACKUP_FOLDER_AUTO")

REQUIRED_TABLES = os.environ.get("TABLE_1"), os.environ.get("TABLE_2"), os.environ.get("TABLE_3")

database_structure = ensure_database_structure(DATABASE, SQL_FOLDER, REQUIRED_TABLES)

def onExit():
    backupDatabase(DATABASE, BACKUP_FOLDER)

def on_keyboard_event(event):
    if event.name == 'e' and event.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl'):
        subprocess.run(["python", "db_structure_sys.py"])
    if event.name == 'b' and event.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl'):
        subprocess.run(["python", "db_backup_sys.py"])


def main():
    keyboard.on_press(on_keyboard_event)
    if database_structure == True:
        subprocess.run(["python", "startPage.py"])
        atexit.register(onExit)

        



if __name__ == '__main__':
    main()