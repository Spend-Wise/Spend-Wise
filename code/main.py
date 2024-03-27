import os
import keyboard
import subprocess

import tkinter as tk

from dotenv import load_dotenv
from database_utils import ensure_database_structure
from registerPage import RegisterPage

load_dotenv()

DATABASE = os.environ.get("DATABASE")
SQL_FOLDER = os.environ.get("SQL_FOLDER")
REQUIRED_TABLES = os.environ.get("TABLE_1"), os.environ.get("TABLE_2"), os.environ.get("TABLE_3")

database_structure = ensure_database_structure(DATABASE, SQL_FOLDER, REQUIRED_TABLES)

def on_keyboard_event(event):
    if event.name == 'e' and event.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl'):
        subprocess.run(["python", "db_structure_sys.py"])  


def main():
    if database_structure == True:
        subprocess.run(["python", "startPage.py"])




if __name__ == '__main__':
    main()