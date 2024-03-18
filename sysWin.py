import os
import json

import sqlite3


from dotenv import load_dotenv

from customtkinter import *
from CTkScrollableDropdown import *
from tkinter import ttk, messagebox

load_dotenv()

DATABASE = os.environ.get("DATABASE")
JSON_FILE = os.environ.get("JSON_FILE")

class Win(CTk):
    def __init__(self):
        super().__init__()

        self.title('Budget Settings')
        self.geometry('1000x580+50+50')
        self.resizable(False, False)
        self.focus_force()

        self.inamountVar = IntVar()
        self.chcategory = StringVar()
        self.expenseLimitVar = IntVar()

        self.formats = ['Select Format', 'JSON', 'Excel File', 'CSV']

        # Frames
        self.titleFrame = CTkFrame(self, width=970, height=50)
        self.titleFrame.place(x=15, y=15)

        self.budgetDetailsFrame = CTkFrame(self, width=470, height=190)
        self.budgetDetailsFrame.place(x=15, y=80)

        self.expenseDetailsFrame = CTkFrame(self, width=470, height=150)
        self.expenseDetailsFrame.place(x=15, y=285)

        self.expenseLimitFrame = CTkFrame(self, width=470, height=115)
        self.expenseLimitFrame.place(x=15, y=450)
        
        self.increaseBudgetFrame = CTkFrame(self, width=470, height=170)
        self.increaseBudgetFrame.place(x=500, y=80)
        
        self.budgetCategoryFrame = CTkFrame(self, width=470, height=115)
        self.budgetCategoryFrame.place(x=500, y=265)

        self.shareExportFrame = CTkFrame(self, width=470, height=170)
        self.shareExportFrame.place(x=500, y=395)
        
        #====================================================================================
        # titleFrame Widgets
        self.title = CTkLabel(self.titleFrame, width=960, height=50, text='Budget Settings', font=('Kameron', 25, 'bold'))
        self.title.place(x=5, y=0)

        #====================================================================================
        # budgetDetailsFrame Widgets
        self.budetalabel = CTkLabel(self.budgetDetailsFrame, text='Budget Details', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.budetalabel.place(x=10, y=5)
        
        self.nameLabel = CTkLabel(self.budgetDetailsFrame, text=f'Name of Budget: ', font=('Kameron', 18, 'bold'))
        self.nameLabel.place(x=10, y=35)

        self.namel = CTkLabel(self.budgetDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.namel.place(x=175, y=35)

        self.dt_label = CTkLabel(self.budgetDetailsFrame, text=f'Date & Time: ', font=('Kameron', 18, 'bold'))
        self.dt_label.place(x=10, y=65)

        self.dtl = CTkLabel(self.budgetDetailsFrame, text='DD/MM/YYYY - HH:MM:SS', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.dtl.place(x=175, y=65)

        self.budamo_label = CTkLabel(self.budgetDetailsFrame, text=f'Total Budget: ', font=('Kameron', 18, 'bold'))
        self.budamo_label.place(x=10, y=95)

        self.bal = CTkLabel(self.budgetDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.bal.place(x=175, y=95)

        self.budrem_label = CTkLabel(self.budgetDetailsFrame, text=f'Remaining Budget: ', font=('Kameron', 18, 'bold'))
        self.budrem_label.place(x=10, y=125)

        self.brl = CTkLabel(self.budgetDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=250, justify='center')
        self.brl.place(x=195, y=125)

        self.cat_label = CTkLabel(self.budgetDetailsFrame, text=f'Budget Category: ', font=('Kameron', 18, 'bold'))
        self.cat_label.place(x=10, y=155)

        self.catl = CTkLabel(self.budgetDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=250, justify='center')
        self.catl.place(x=195, y=155)


        #=====================================================================
        # expenseDetailsFrame Widgets
        self.latestexplabel = CTkLabel(self.expenseDetailsFrame, text='Latest Expense', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.latestexplabel.place(x=10, y=5)

        self.eamoLabel = CTkLabel(self.expenseDetailsFrame, text=f'Amount: ', font=('Kameron', 18, 'bold'))
        self.eamoLabel.place(x=10, y=35)

        self.eamol = CTkLabel(self.expenseDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.eamol.place(x=175, y=35)

        self.edt_label = CTkLabel(self.expenseDetailsFrame, text=f'Date & Time: ', font=('Kameron', 18, 'bold'))
        self.edt_label.place(x=10, y=65)

        self.edtl = CTkLabel(self.expenseDetailsFrame, text='DD/MM/YYYY - HH:MM:SS', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.edtl.place(x=175, y=65)

        self.ecat_label = CTkLabel(self.expenseDetailsFrame, text=f'Expense Category: ', font=('Kameron', 18, 'bold'))
        self.ecat_label.place(x=10, y=95)

        self.ecatl = CTkLabel(self.expenseDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=250, justify='center')
        self.ecatl.place(x=195, y=95)

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

        self.eamol = CTkLabel(self.increaseBudgetFrame, text='----', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.eamol.place(x=175, y=65)

        self.edt_label = CTkLabel(self.increaseBudgetFrame, text=f'Total Budget Remaining: ', font=('Kameron', 18, 'bold'))
        self.edt_label.place(x=10, y=95)

        self.edtl = CTkLabel(self.increaseBudgetFrame, text='----', font=('Kameron', 18, 'bold'), width=200, justify='center')
        self.edtl.place(x=250, y=95)

        self.inBtn = CTkButton(self.increaseBudgetFrame, text='Increase Budget', font=('Kameron', 18, 'bold'), width=450)
        self.inBtn.place(x=10, y=130)

        #=====================================================================================
        # budgetCategoryFrame Widgets
        self.cate_label = CTkLabel(self.budgetCategoryFrame, text='Change Category', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.cate_label.place(x=10, y=5)

        self.categlabel = CTkLabel(self.budgetCategoryFrame, text=f'Change Category to : ', font=('Kameron', 18, 'bold'))
        self.categlabel.place(x=10, y=35)

        self.cateEnt = CTkEntry(self.budgetCategoryFrame, width=190, font=('Kameron', 18), textvariable=self.chcategory)
        self.cateEnt.place(x=250, y=35)

        self.inBtn = CTkButton(self.budgetCategoryFrame, text='Change Category', font=('Kameron', 18, 'bold'), width=450)
        self.inBtn.place(x=10, y=75)

        #=============================================================================
        # expenseLimitFrame Widgets
        self.cate_label = CTkLabel(self.expenseLimitFrame, text='One Time Expesense Limit', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.cate_label.place(x=10, y=5)

        self.categlabel = CTkLabel(self.expenseLimitFrame, text=f'Limit: ', font=('Kameron', 18, 'bold'))
        self.categlabel.place(x=10, y=35)

        self.cateEnt = CTkEntry(self.expenseLimitFrame, width=190, font=('Kameron', 18), textvariable=self.expenseLimitVar)
        self.cateEnt.place(x=250, y=35)

        self.inBtn = CTkButton(self.expenseLimitFrame, text='Set Limit', font=('Kameron', 18, 'bold'), width=450)
        self.inBtn.place(x=10, y=75)

        #=====================================================================================
        # shareExportFrame Widgets
        self.se_label = CTkLabel(self.shareExportFrame, text='Share & Export Budget', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.se_label.place(x=10, y=5)

        self.expaslabel = CTkLabel(self.shareExportFrame, text=f'Export as: ', font=('Kameron', 18, 'bold'))
        self.expaslabel.place(x=10, y=45)

        self.expasEnt = CTkComboBox(self.shareExportFrame, width=280, font=('Kameron', 17))
        self.expasEnt.place(x=175, y=45)

        self.sd = CTkScrollableDropdownFrame(self.expasEnt, values=self.formats, justify="left", button_color="transparent", autocomplete=True, x=-57.5, y=-50)


        self.expBtn = CTkButton(self.shareExportFrame, text='Export Budget', font=('Kameron', 18, 'bold'), width=450)
        self.expBtn.place(x=10, y=85)

        self.shaBtn = CTkButton(self.shareExportFrame, text='Share Budget', font=('Kameron', 18, 'bold'), width=450)
        self.shaBtn.place(x=10, y=125)

        # Funciton Calls
        self.setData()

    def getBudgetID(self):
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
    
        return data['budget_id']
    
    def setData(self):
        budget_id = self.getBudgetID()
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            getQuery = 'SELECT * FROM budget WHERE budget_id=?'
            valuesGQ = (budget_id, )

            cursor.execute(getQuery, valuesGQ)
            data = cursor.fetchone()

            print(data)

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error (loadBudgetCards)", f"{e}")

        finally:
            if conn:
                conn.close()




if __name__ == '__main__':
    win = Win()
    win.mainloop()