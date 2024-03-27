import os
import sqlite3

from dotenv import load_dotenv

from customtkinter import *
from tkinter import ttk, messagebox

load_dotenv()

DATABASE = os.environ.get("DATABASE")

class DBStructure(CTk):
    def __init__(self):
        super().__init__()
        
        self.db_score = 0

        self.title('Database Structure System')
        self.geometry('490x350+50+50')
        self.resizable(False, False)
        self.focus_force()

        self.titleFrame = CTkFrame(self, width=460, height=50)
        self.titleFrame.place(x=15, y=15)

        self.checksFrame = CTkFrame(self, width=460, height=200)
        self.checksFrame.place(x=15, y=80)

        self.statusFrame = CTkFrame(self, width=460, height=40)
        self.statusFrame.place(x=15, y=295)

        self.title = CTkLabel(self.titleFrame, width=440, height=50, text='Database Structure', font=('Kameron', 25, 'bold'))
        self.title.place(x=5, y=0)

        self.database = CTkLabel(self.checksFrame, text='Database', font=('Kameron', 17, 'bold'), width=112)
        self.database.place(x=174, y=15)

        self.registration = CTkLabel(self.checksFrame, text='Registration', font=('Kameron', 17, 'bold'), width=112)
        self.registration.place(x=17, y=115)

        self.budget = CTkLabel(self.checksFrame, text='Budget', font=('Kameron', 17, 'bold'), width=112)
        self.budget.place(x=174, y=115)

        self.expense = CTkLabel(self.checksFrame, text='Expense', font=('Kameron', 18, 'bold'), width=120)
        self.expense.place(x=330, y=115)

        self.db = IntVar()
        self.rg = IntVar()
        self.bg = IntVar()
        self.ex = IntVar()

        self.db_ch = CTkCheckBox(self.checksFrame, text='', state='disabled', onvalue=1, offvalue=0, variable=self.db)
        self.db_ch.place(x=218, y=55)

        self.rg_ch = CTkCheckBox(self.checksFrame, text='', state='disabled', onvalue=1, offvalue=0, variable=self.rg)
        self.rg_ch.place(x=60, y=155)

        self.bg_ch = CTkCheckBox(self.checksFrame, text='', state='disabled', onvalue=1, offvalue=0, variable=self.bg)
        self.bg_ch.place(x=218, y=155)

        self.ex_ch = CTkCheckBox(self.checksFrame, text='', state='disabled', onvalue=1, offvalue=0, variable=self.ex)
        self.ex_ch.place(x=380, y=155)

        self.stat = CTkLabel(self.statusFrame, text='Status: ', font=('Kameron', 17, 'bold'), justify='right', width=220)
        self.stat.place(x=10, y=5)

        self.status = CTkLabel(self.statusFrame, font=('Kameron', 20, 'bold'), justify='left', width=220)
        self.status.place(x=220, y=5)

        if self.check('registration'):
            self.rg.set(1)
            self.db_score += 1

        if self.check('budget'):
            self.bg.set(1)
            self.db_score += 1

        if self.check('expense'):
            self.ex.set(1)
            self.db_score += 1

        if self.db_score  == 3:
            self.db.set(1)
            self.status.configure(text='GOOD', text_color='green')
        if self.db_score  < 3:
            self.db.set(0)
            self.status.configure(text='NOT GOOD', text_color='red')

    def check(self, table_name):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            result = cursor.fetchone()
            conn.close()
            return result is not None


        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

if __name__ == '__main__':
    dbs = DBStructure()
    dbs.mainloop()