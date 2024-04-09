import os
import sqlite3
import platform
import subprocess

from dotenv import load_dotenv
from PIL import Image

from database_utils import restoreDatabase

from customtkinter import *
from tkinter import ttk, messagebox

from CTkToolTip import *

load_dotenv()

DATABASE = os.environ.get("DATABASE")
BACKUP_FOLDER = os.environ.get("DATABASE_BACKUP_FOLDER_AUTO")

class DBBackup(CTk):
    def __init__(self):
        super().__init__()
        
        self.db_score = 0

        self.title('Database Backup System')
        self.geometry('490x350+50+50')
        self.resizable(False, False)
        self.focus_force()

        # image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        # info_light = Image.open(os.path.join(image_path, "info_light.png"))
        # info_dark = Image.open(os.path.join(image_path, "info_dark.png"))

        # self.infoImg = CTkImage(light_image=info_light, dark_image=info_dark, size=(15, 15))


        self.mainTabview = CTkTabview(self, 450, 315)
        self.mainTabview.place(x=20, y=20)

        self.mainTabview._segmented_button.configure(font=('Kameron', 17, 'bold'))

        self.mainTabview.add('AUTO')
        self.mainTabview.add('USER')

        self.noteText = 'This tab only shows the information about the last backup which is created automatically everytime after the application is closed.'

        auto = self.mainTabview.tab('AUTO')

        # self.i = CTkLabel(self.mainTabview, text='', font=('Kameron', 17, 'bold'), fg_color='transparent', image=self.infoImg)
        # self.i.place(x=425, y=20)

        

        # AUTO =========================================================================================================
        fname_label = CTkLabel(auto, text='File Name: ', font=('Kameron', 17, 'bold'), width=210)
        fname_label.place(x=5, y=10)

        self.fileName = CTkLabel(auto, text='[Name Here]', font=('Kameron', 17, 'bold'), width=215)
        self.fileName.place(x=220, y=10)

        fdate_label = CTkLabel(auto, text='Last Backup Date: ', font=('Kameron', 17, 'bold'), width=210)
        fdate_label.place(x=5, y=50)

        self.fileDate = CTkLabel(auto, text='[Date Here]', font=('Kameron', 17, 'bold'), width=215)
        self.fileDate.place(x=220, y=50)

        ftime_label = CTkLabel(auto, text='Last Backup Time: ', font=('Kameron', 17, 'bold'), width=210)
        ftime_label.place(x=5, y=90)

        self.fileTime = CTkLabel(auto, text='[Time Here]', font=('Kameron', 17, 'bold'), width=215)
        self.fileTime.place(x=220, y=90)

        self.loadButton = CTkButton(auto, text='Load This Backup', font=('Kameron', 17, 'bold'), width=420, command=self.loadBackup)
        self.loadButton.place(x=10, y=130)
        CTkToolTip(self.loadButton, 'Clicking on this button will load the contents of the latest backup file to the main database.', border_width=2, wraplength=210)

        self.viewButton = CTkButton(auto, text='View Backup File', font=('Kameron', 17, 'bold'), width=420, command=self.open_folder)
        self.viewButton.place(x=10, y=170)
        CTkToolTip(self.viewButton, 'Opens the location of the Backup file in the File Explorer.', border_width=2, wraplength=210)

        self.noteLabel = CTkLabel(auto, text='Note :', width=50, font=('Kameron', 15, 'bold'))
        self.noteLabel.place(x=5, y=210)


        self.note = CTkLabel(auto, font=('Kameron', 15, 'bold'), width=355, wraplength=355, text=self.noteText)
        self.note.place(x=65, y=210)

    def loadBackup(self):
        backupfile = os.path.join(BACKUP_FOLDER, 'spendwise.db.bak')

        restoreDatabase(backupfile, DATABASE)
        messagebox.showinfo('Loaded', 'Backup Loaded Successfully!!!')

    def open_folder(self):
        folder_path = 'D:/DurgeshFiles/Spend-Wise/code/backup/database/auto'
        system_platform = platform.system()
        if system_platform == "Windows":
            os.startfile(folder_path)
        elif system_platform == "Darwin":  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # Linux
            subprocess.Popen(["xdg-open", folder_path])

    

if __name__ == '__main__':
    dbs = DBBackup()
    dbs.mainloop()