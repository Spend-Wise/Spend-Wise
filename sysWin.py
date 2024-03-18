import os
import sqlite3

from dotenv import load_dotenv

from customtkinter import *
from tkinter import ttk, messagebox

load_dotenv()

DATABASE = os.environ.get("DATABASE")

class Win(CTk):
    def __init__(self):
        super().__init__()

        self.title('Budget Settings')
        self.geometry('500x580+50+50')
        self.resizable(False, False)
        self.focus_force()

        self.inamountVar = IntVar()

        # Frames
        self.titleFrame = CTkFrame(self, width=470, height=50)
        self.titleFrame.place(x=15, y=15)

        self.budgetDetailsFrame = CTkFrame(self, width=470, height=250)
        self.budgetDetailsFrame.place(x=15, y=80)

        self.increaseBudgetFrame = CTkFrame(self, width=470, height=170)
        self.increaseBudgetFrame.place(x=15, y=345)

        self.buttonsFrame = CTkFrame(self, width=470, height=40)
        self.buttonsFrame.place(x=15, y=530)
        
        #====================================================================================
        # titleFrame Widgets
        self.title = CTkLabel(self.titleFrame, width=460, height=50, text='Budget Settings', font=('Kameron', 25, 'bold'))
        self.title.place(x=5, y=0)

        #====================================================================================
        # budgetDetailsFrame Widgets
        self.budetalabel = CTkLabel(self.budgetDetailsFrame, text='Budget Details', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.budetalabel.place(x=10, y=5)
        
        self.nameLabel = CTkLabel(self.budgetDetailsFrame, text=f'Name of Budget: ', font=('Kameron', 18, 'bold'))
        self.nameLabel.place(x=10, y=35)

        self.namel = CTkLabel(self.budgetDetailsFrame, text='bud 1', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.namel.place(x=175, y=35)

        self.dt_label = CTkLabel(self.budgetDetailsFrame, text=f'Date & Time: ', font=('Kameron', 18, 'bold'))
        self.dt_label.place(x=10, y=65)

        self.dtl = CTkLabel(self.budgetDetailsFrame, text='DD/MM/YYYY - HH:MM:SS', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.dtl.place(x=175, y=65)

        self.budamo_label = CTkLabel(self.budgetDetailsFrame, text=f'Total Budget: ', font=('Kameron', 18, 'bold'))
        self.budamo_label.place(x=10, y=95)

        self.bal = CTkLabel(self.budgetDetailsFrame, text='$700,000', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.bal.place(x=175, y=95)

        self.budrem_label = CTkLabel(self.budgetDetailsFrame, text=f'Remaining Budget: ', font=('Kameron', 18, 'bold'))
        self.budrem_label.place(x=10, y=125)

        self.brl = CTkLabel(self.budgetDetailsFrame, text='$548,512', font=('Kameron', 18, 'bold'), width=250, justify='center')
        self.brl.place(x=195, y=125)

        self.latestexplabel = CTkLabel(self.budgetDetailsFrame, text='Latest Expense', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.latestexplabel.place(x=10, y=155)

        self.eamoLabel = CTkLabel(self.budgetDetailsFrame, text=f'Amount: ', font=('Kameron', 18, 'bold'))
        self.eamoLabel.place(x=10, y=185)

        self.eamol = CTkLabel(self.budgetDetailsFrame, text='$45,000', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.eamol.place(x=175, y=185)

        self.edt_label = CTkLabel(self.budgetDetailsFrame, text=f'Date & Time: ', font=('Kameron', 18, 'bold'))
        self.edt_label.place(x=10, y=215)

        self.edtl = CTkLabel(self.budgetDetailsFrame, text='DD/MM/YYYY - HH:MM:SS', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.edtl.place(x=175, y=215)

        #=====================================================================================
        # increaseBudgetFrame Widgets
        self.inbudlabel = CTkLabel(self.increaseBudgetFrame, text='Increase Budget', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.inbudlabel.place(x=10, y=5)

        self.inamol = CTkLabel(self.increaseBudgetFrame, text=f'Increse Budget Quota by : ', font=('Kameron', 18, 'bold'))
        self.inamol.place(x=10, y=35)

        self.entamo = CTkEntry(self.increaseBudgetFrame, width=190, font=('Kameron', 18), textvariable=self.inamountVar)
        self.entamo.place(x=250, y=35)

        self.tbudlab = CTkLabel(self.increaseBudgetFrame, text=f'Total Budget: ', font=('Kameron', 18, 'bold'))
        self.tbudlab.place(x=10, y=65)

        self.eamol = CTkLabel(self.increaseBudgetFrame, text='$45,000', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.eamol.place(x=175, y=65)

        self.edt_label = CTkLabel(self.increaseBudgetFrame, text=f'Total Budget Remaining: ', font=('Kameron', 18, 'bold'))
        self.edt_label.place(x=10, y=95)

        self.edtl = CTkLabel(self.increaseBudgetFrame, text='$45,000', font=('Kameron', 18, 'bold'), width=200, justify='center')
        self.edtl.place(x=250, y=95)

        self.inBtn = CTkButton(self.increaseBudgetFrame, text='Increase Budget', font=('Kameron', 18, 'bold'), width=450)
        self.inBtn.place(x=10, y=130)

        #=====================================================================================
        # buttonsFrame Widgets
        self.expBtn = CTkButton(self.buttonsFrame, text='Export Budget', font=('Kameron', 18, 'bold'), width=228)
        self.expBtn.place(x=5, y=5)

        self.shaBtn = CTkButton(self.buttonsFrame, text='Share Budget', font=('Kameron', 18, 'bold'), width=228)
        self.shaBtn.place(x=238, y=5)


if __name__ == '__main__':
    win = Win()
    win.mainloop()