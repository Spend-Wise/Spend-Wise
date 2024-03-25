import os
import csv
import json

import sqlite3

import pandas as pd

from dotenv import load_dotenv

from PIL import Image
from customtkinter import *
from CTkScrollableDropdown import *
from tkinter import ttk, messagebox

load_dotenv()

DATABASE = os.environ.get("DATABASE")
JSON_FILE = os.environ.get("JSON_FILE")
CDJSON_FILE = os.environ.get("CURRENT_DATA_JSON_FILE")

class Win(CTk):
    def __init__(self):
        super().__init__()

        self.title('Budget Settings')
        self.geometry('985x610+50+50')
        self.resizable(False, False)
        self.focus_force()

        self.inamountVar = StringVar()
        self.chcategory = StringVar()
        self.expenseLimitVar = StringVar()

        self.formats = ['Select Format', 'JSON', 'Excel File', 'CSV']

        # Images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        edit_light = Image.open(os.path.join(image_path, "edit_light.png"))
        edit_dark = Image.open(os.path.join(image_path, "edit_dark.png"))

        self.editImg = CTkImage(light_image=edit_light, dark_image=edit_dark, size=(20, 20))

        # Frames
        self.titleFrame = CTkFrame(self, width=955, height=50)
        self.titleFrame.place(x=15, y=15)

        self.budgetDetailsFrame = CTkFrame(self, width=470, height=190)
        self.budgetDetailsFrame.place(x=15, y=80)

        self.expenseDetailsFrame = CTkFrame(self, width=470, height=150)
        self.expenseDetailsFrame.place(x=15, y=285)

        self.expenseLimitFrame = CTkFrame(self, width=470, height=145)
        self.expenseLimitFrame.place(x=15, y=450)
        
        self.increaseBudgetFrame = CTkFrame(self, width=470, height=170)
        self.increaseBudgetFrame.place(x=500, y=80)
        
        self.budgetCategoryFrame = CTkFrame(self, width=470, height=115)
        self.budgetCategoryFrame.place(x=500, y=265)

        self.shareExportFrame = CTkFrame(self, width=470, height=200)
        self.shareExportFrame.place(x=500, y=395)
        
        #====================================================================================
        # titleFrame Widgets
        self.title = CTkLabel(self.titleFrame, width=945, height=50, text='Budget Settings', font=('Kameron', 25, 'bold'))
        self.title.place(x=5, y=0)

        #====================================================================================
        # budgetDetailsFrame Widgets
        self.budetalabel = CTkLabel(self.budgetDetailsFrame, text='Budget Details', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.budetalabel.place(x=10, y=5)
        
        self.nameLabel = CTkLabel(self.budgetDetailsFrame, text=f'Name of Budget: ', font=('Kameron', 18, 'bold'))
        self.nameLabel.place(x=10, y=35)

        self.namel = CTkLabel(self.budgetDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.namel.place(x=175, y=35)

        # self.ednm = CTkButton(self.budgetDetailsFrame, width=30, text='', image=self.editImg, command=self.editBudName)
        # self.ednm.place(x=425, y=35)

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

        self.enameLabel = CTkLabel(self.expenseDetailsFrame, text=f'Name: ', font=('Kameron', 18, 'bold'))
        self.enameLabel.place(x=10, y=35)

        self.enaml = CTkLabel(self.expenseDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.enaml.place(x=175, y=35)

        self.eamoLabel = CTkLabel(self.expenseDetailsFrame, text=f'Amount: ', font=('Kameron', 18, 'bold'))
        self.eamoLabel.place(x=10, y=65)

        self.eamol = CTkLabel(self.expenseDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.eamol.place(x=175, y=65)

        self.edt_label = CTkLabel(self.expenseDetailsFrame, text=f'Date & Time: ', font=('Kameron', 18, 'bold'))
        self.edt_label.place(x=10, y=95)

        self.edtl = CTkLabel(self.expenseDetailsFrame, text='DD/MM/YYYY - HH:MM:SS', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.edtl.place(x=175, y=95)

        self.ecat_label = CTkLabel(self.expenseDetailsFrame, text=f'Expense Category: ', font=('Kameron', 18, 'bold'))
        self.ecat_label.place(x=10, y=120)

        self.ecatl = CTkLabel(self.expenseDetailsFrame, text='----', font=('Kameron', 18, 'bold'), width=250, justify='center')
        self.ecatl.place(x=195, y=120)

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

        self.tbudl = CTkLabel(self.increaseBudgetFrame, text='----', font=('Kameron', 18, 'bold'), width=280, justify='center')
        self.tbudl.place(x=175, y=65)

        self.edt_label = CTkLabel(self.increaseBudgetFrame, text=f'Total Budget Remaining: ', font=('Kameron', 18, 'bold'))
        self.edt_label.place(x=10, y=95)

        self.tbrl = CTkLabel(self.increaseBudgetFrame, text='----', font=('Kameron', 18, 'bold'), width=200, justify='center')
        self.tbrl.place(x=250, y=95)

        self.inBtn = CTkButton(self.increaseBudgetFrame, text='Increase Budget', font=('Kameron', 18, 'bold'), width=450, command=self.increaseBudget)
        self.inBtn.place(x=10, y=130)

        #=====================================================================================
        # budgetCategoryFrame Widgets
        self.cate_label = CTkLabel(self.budgetCategoryFrame, text='Change Category', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.cate_label.place(x=10, y=5)

        self.categlabel = CTkLabel(self.budgetCategoryFrame, text=f'Change Category to : ', font=('Kameron', 18, 'bold'))
        self.categlabel.place(x=10, y=35)

        self.cateEnt = CTkEntry(self.budgetCategoryFrame, width=190, font=('Kameron', 18), textvariable=self.chcategory)
        self.cateEnt.place(x=250, y=35)

        self.chBtn = CTkButton(self.budgetCategoryFrame, text='Change Category', font=('Kameron', 18, 'bold'), width=450, command=self.changeCategory)
        self.chBtn.place(x=10, y=75)

        #=============================================================================
        # expenseLimitFrame Widgets
        self.cate_label = CTkLabel(self.expenseLimitFrame, text='One Time Expesense Limit', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.cate_label.place(x=10, y=5)

        self.celt_label = CTkLabel(self.expenseLimitFrame, text=f'Current Expense Limit: ', font=('Kameron', 18, 'bold'))
        self.celt_label.place(x=10, y=35)

        self.cell = CTkLabel(self.expenseLimitFrame, text='----', font=('Kameron', 18, 'bold'), width=200, justify='center')
        self.cell.place(x=250, y=35)

        self.categlabel = CTkLabel(self.expenseLimitFrame, text=f'Limit: ', font=('Kameron', 18, 'bold'))
        self.categlabel.place(x=10, y=65)

        self.cateEnt = CTkEntry(self.expenseLimitFrame, width=190, font=('Kameron', 18), textvariable=self.expenseLimitVar)
        self.cateEnt.place(x=250, y=65)

        self.inBtn = CTkButton(self.expenseLimitFrame, text='Set Limit', font=('Kameron', 18, 'bold'), width=450, command=self.changeOTExpLim)
        self.inBtn.place(x=10, y=105)

        #=====================================================================================
        # shareExportFrame Widgets
        self.se_label = CTkLabel(self.shareExportFrame, text='Budget Options', font=('Kameron', 22, 'bold'), width=450, justify='center')
        self.se_label.place(x=10, y=5)

        self.expaslabel = CTkLabel(self.shareExportFrame, text=f'Export as: ', font=('Kameron', 18, 'bold'))
        self.expaslabel.place(x=10, y=45)

        self.expasEnt = CTkComboBox(self.shareExportFrame, width=280, font=('Kameron', 17))
        self.expasEnt.place(x=175, y=45)

        self.sd = CTkScrollableDropdownFrame(self.expasEnt, values=self.formats, justify="left", button_color="transparent", autocomplete=True, x=-57.5, y=-50)

        self.expBtn = CTkButton(self.shareExportFrame, text='Export Budget', font=('Kameron', 18, 'bold'), width=450, command=self.exportBudget)
        self.expBtn.place(x=10, y=85)

        self.shaBtn = CTkButton(self.shareExportFrame, text='Share Budget', font=('Kameron', 18, 'bold'), width=450)
        self.shaBtn.place(x=10, y=125)

        self.archBtn = CTkButton(self.shareExportFrame, text='Archive Budget', font=('Kameron', 18, 'bold'), width=450, fg_color='#1f8d3b', hover_color='#155c21', command=lambda budget_id=self.getBudgetID(): self.archive(budget_id) )
        self.archBtn.place(x=10, y=165)

        # Funciton Calls
        self.setData()
        # self.updateAmounts()

        # Binding
        self.entamo.bind('<KeyRelease>', self.setzero)
        self.entamo.bind('<KeyRelease>', self.updateAmounts)

    def getBudgetID(self):
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
    
        return data['budget_id']
    
    def setData(self):
        budget_id = self.getBudgetID()
        self.setArchive(budget_id)
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()


            # Queries and Values
            getQuery = 'SELECT * FROM budget WHERE budget_id=?'
            valuesGQ = (budget_id, )

            #------------------------------------------------------------------------------------------

            cursor.execute(getQuery, valuesGQ)
            dataGQ = cursor.fetchone()

            if dataGQ:
                budgetid, user_id, name, amount, category, used, date, time, expLimit, arch = dataGQ

                dateTime = f"{date}  -  {time}"
                remainingBudget = amount - used

                self.namel.configure(text=str(name))
                self.dtl.configure(text=str(dateTime))
                self.bal.configure(text=f"${'{:,}'.format(amount)}")
                self.brl.configure(text=f"${'{:,}'.format(remainingBudget)}")
                self.catl.configure(text=str(category))

                self.cell.configure(text=f"${'{:,}'.format(expLimit)}")

                self.setBudJSON(budgetid, user_id, name, amount, category, used, date, time, expLimit, arch)
                #-------------------------------------------------------------------------------------

                ExpQuery = 'SELECT * FROM expense WHERE budget_id = ? ORDER BY date DESC, time DESC LIMIT 1'
                valuesEQ= (budgetid, )

                cursor.execute(ExpQuery, valuesEQ)
                dataEQ = cursor.fetchone()

                # print(dataEQ)

                if dataEQ:
                    expID, budID, expName, expAmo, expCat, expDt, expTm = dataEQ

                    exDateTime = f'{expDt}  -  {expTm}'
                    
                    self.enaml.configure(text=str(expName))
                    self.eamol.configure(text=f"${'{:,}'.format(expAmo)}")
                    self.edtl.configure(text=str(exDateTime))
                    self.ecatl.configure(text=str(expCat))

                    self.setExpJSON(expID, budID, expName, expAmo, expCat, expDt, expTm)                

            # print(data)

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def setBudJSON(self, budget_id, user_id, budName, budAmo, budCat, budUsed, budDate, budTime, budEL, budArch):
        with open(CDJSON_FILE, 'r') as file:
            data = json.load(file)
            
        data['budget']['budget_id'] = budget_id
        data['budget']['user_id'] = user_id
        data['budget']['budget_name'] = budName
        data['budget']['budget_amount'] = budAmo
        data['budget']['budget_category'] = budCat
        data['budget']['budget_status'] = budUsed
        data['budget']['date'] = budDate
        data['budget']['time'] = budTime
        data['budget']['expense_limit'] = budEL
        data['budget']['archived'] = budArch
        
        with open(CDJSON_FILE, 'w') as file:
            json.dump(data, file)

    def setExpJSON(self, expID, budID, expName, expAmo, expCate, expDate, expTime):
        with open(CDJSON_FILE, 'r') as file:
            data = json.load(file)
            
        data['latestExpense']['expense_id'] = expID
        data['latestExpense']['budget_id'] = budID
        data['latestExpense']['expense_name'] = expName
        data['latestExpense']['expense_amount'] = expAmo
        data['latestExpense']['expense_category'] = expCate
        data['latestExpense']['date'] = expDate
        data['latestExpense']['time'] = expTime
        
        with open(CDJSON_FILE, 'w') as file:
            json.dump(data, file)

    def changeOTExpLim(self):
        newLimit = int(self.expenseLimitVar.get())
        budget_id = self.getBudgetID()

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            getQuery = "SELECT budget_amount, budget_name FROM budget WHERE budget_id=?"
            valuesGQ = (budget_id, )

            cursor.execute(getQuery, valuesGQ)
            data = cursor.fetchone()

            if data:
                budAmo, budName = data

            updateQuery = 'UPDATE budget SET expense_limit=? WHERE budget_id=?'
            valuesUQ = (newLimit, budget_id)

            
            if newLimit == '':
                pass

            if newLimit > int(budAmo):
                messagebox.showerror('Invalid Input', 'The value you have eneterd is more than the Alloted budget it self. Please enter value less than the Alloted Budget.')
            else:
                cursor.execute(updateQuery, valuesUQ)
                conn.commit()
                messagebox.showinfo('Expense Limit Increased', f'Expense Limit of {budName} has been changed to {newLimit}.')
                self.setData()
                self.expenseLimitVar.set(0)
            

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def changeCategory(self):
        newCatergory = self.chcategory.get()
        budget_id = self.getBudgetID()

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            getQuery = "SELECT budget_amount, budget_name FROM budget WHERE budget_id=?"
            valuesGQ = (budget_id, )

            cursor.execute(getQuery, valuesGQ)
            data = cursor.fetchone()

            if data:
                budAmo, budName = data

            updateQuery = 'UPDATE budget SET budget_category=? WHERE budget_id=?'
            valuesUQ = (newCatergory, budget_id)

            if newCatergory == '':
                messagebox.showerror('Invalid Input', 'Please Enter Valid Category Name.')
            else:
                cursor.execute(updateQuery, valuesUQ)
                conn.commit()
                messagebox.showinfo('Category changed', f'Category of {budName} has been changed to {newCatergory}.')
                self.setData()
                self.chcategory.set("")
            

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def increaseBudget(self):
        newBudget = int(self.inamountVar.get())
        budget_id = self.getBudgetID()

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            getQuery = "SELECT budget_amount, budget_name FROM budget WHERE budget_id=?"
            valuesGQ = (budget_id, )

            cursor.execute(getQuery, valuesGQ)
            data = cursor.fetchone()

            if data:
                budAmo, budName = data

            totalBudAmo = budAmo + newBudget

            updateQuery = 'UPDATE budget SET budget_amount=? WHERE budget_id=?'
            valuesUQ = (totalBudAmo, budget_id)

            if newBudget == 0:
                messagebox.showerror('Invalid Input', 'Please Enter Valid Budget amount')
            else:
                
                cursor.execute(updateQuery, valuesUQ)
                conn.commit()
                
                messagebox.showinfo('Budget Increased', f'Budget of {budName} has been inccreased by {newBudget}. Now the total Budget amount is {totalBudAmo}')
                self.setData()
                self.inamountVar.set(0)
            

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def updateAmounts(self, event):
        amount = int(self.inamountVar.get())
        budget_id = self.getBudgetID()
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            getQuery = "SELECT budget_amount, budget_status FROM budget WHERE budget_id=?"
            valuesGQ = (budget_id, )

            cursor.execute(getQuery, valuesGQ)
            data = cursor.fetchone()

            if data:
                budAmo, budUsed = data

            
            if amount != '':
                totalAmount = budAmo + amount
                totalRemainingAmount = totalAmount - budUsed

                self.tbudl.configure(text=f"${'{:,}'.format(totalAmount)}")
                self.tbrl.configure(text=f"${'{:,}'.format(totalRemainingAmount)}")

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()
    
    def setzero(self, event):
        if self.inamountVar.get() == '':
            self.inamountVar.set(0)

    def archive(self, budget_id):
        archY = 'yes'
        archN = 'no'
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            getQuery = "SELECT archived, budget_name FROM budget WHERE budget_id=?"
            valuesGQ = (budget_id, )

            cursor.execute(getQuery, valuesGQ)
            data = cursor.fetchone()

            if data:
                archived, budName = data

                if archived == 'no':
                    setQuery = "UPDATE budget SET archived=? WHERE budget_id=?"
                    valuesSQ = (archY, budget_id, )

                    cursor.execute(setQuery, valuesSQ)
                    conn.commit()

                    with open(CDJSON_FILE, 'r') as file:
                        data = json.load(file)
                    
                    data['budget']['archived'] = 'yes'
                    
                    with open(CDJSON_FILE, 'w') as file:
                        json.dump(data, file)

                    messagebox.showinfo('Budget Archived', f'{budName} has been ARCHIVED. To see the archived budgets please click on the Archived Budgets Tab in the navigation menu.')
                    self.archBtn.configure(text='Unarchive Budget')
                    sys.exit()

                else:
                    setQuery = "UPDATE budget SET archived=? WHERE budget_id=?"
                    valuesSQ = (archN, budget_id, )

                    with open(CDJSON_FILE, 'r') as file:
                        data = json.load(file)
                    
                    data['budget']['archived'] = 'no'
                    
                    with open(CDJSON_FILE, 'w') as file:
                        json.dump(data, file)

                    cursor.execute(setQuery, valuesSQ)
                    conn.commit()
                    messagebox.showinfo('Budget Archived', f'{budName} has been UNARCHIVED.')
                    self.archBtn.configure(text='Archive Budget')
                    sys.exit()

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()
    
    def setArchive(self, budget_id):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            getQuery = "SELECT archived, budget_name FROM budget WHERE budget_id=?"
            valuesGQ = (budget_id, )

            cursor.execute(getQuery, valuesGQ)
            data = cursor.fetchone()

            if data:
                archived, budName = data

                if archived == 'no':
                    self.archBtn.configure(text='Archive Budget')

                else:
                    self.archBtn.configure(text='Unarchive Budget')
            

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def add_zero(self, number):
        if len(str(number).split('.')[0]) == 1:
            return "0" + str(number)
        else:
            return str(number)

    def exportBudget(self):
        exportType = self.getExportType()

        if exportType == 'JSON':
            self.JSONExport()

        elif exportType == 'CSV':
            self.CSVExport()

        elif exportType == 'Excel File':
            self.excelExport()

    def getExportType(self):
        exportType = self.expasEnt.get()
        
        if exportType == 'Select Format':
            messagebox.showerror('Invalid Export Format', 'Please select an Valid export Format.')
        else:
            return exportType

    def JSONExport(self):
        budget_id = self.getBudgetID()
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM budget WHERE budget_id = ?", (budget_id,))
            budget_fields = [description[0] for description in cursor.description] 
            budget_data = cursor.fetchone()

            cursor.execute("SELECT * FROM expense WHERE budget_id = ?", (budget_id,))
            expense_fields = [description[0] for description in cursor.description]  # Get the field names
            expense_data = cursor.fetchall()

            budget_dict = {field: value for field, value in zip(budget_fields, budget_data)}
            expenses_list = [{field: value for field, value in zip(expense_fields, expense)} for expense in expense_data]

            data_to_export = {
                "budget": budget_dict,
                "expenses": expenses_list
            }

            folder_path = 'exports/json'
            os.makedirs(folder_path, exist_ok=True)

            filePath = os.path.join(folder_path, f"EXPD_{budget_id}.json")
            
            with open(filePath, "w") as json_file:
                json.dump(data_to_export, json_file, indent=4)

                messagebox.showinfo('Budget Exported', 'Budget has been successfully Exported as JSON file.')

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def CSVExport(self):
        budget_id = self.getBudgetID()
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM budget WHERE budget_id = ?", (budget_id,))
            budget_fields = [description[0] for description in cursor.description] 
            budget_data = cursor.fetchone()

            cursor.execute("SELECT * FROM expense WHERE budget_id = ?", (budget_id,))
            expense_fields = [description[0] for description in cursor.description]  # Get the field names
            expense_data = cursor.fetchall()

            budget_dict = {field: value for field, value in zip(budget_fields, budget_data)}
            expenses_list = [{field: value for field, value in zip(expense_fields, expense)} for expense in expense_data]

            folder_path = f'exports/csv/{budget_id}'
            os.makedirs(folder_path, exist_ok=True)

            budget_file_path = os.path.join(folder_path, f"EXPBD_{budget_id}.csv")
            expenses_file_path = os.path.join(folder_path, f"EXPED_{budget_id}.csv")

            # Write budget data to CSV
            with open(budget_file_path, 'w', newline='') as budget_file:
                writer = csv.DictWriter(budget_file, fieldnames=budget_fields)
                writer.writeheader()
                writer.writerow(budget_dict)

            # Write expenses data to CSV
            with open(expenses_file_path, 'w', newline='') as expenses_file:
                writer = csv.DictWriter(expenses_file, fieldnames=expense_fields)
                writer.writeheader()
                writer.writerows(expenses_list)

            messagebox.showinfo('Budget Exported', 'Budget has been successfully Exported as CSV.')

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def excelExport(self):
        budget_id = self.getBudgetID()
        conn = sqlite3.connect(DATABASE)
        query_budget = f"SELECT * FROM budget WHERE budget_id = {budget_id}"
        
        # Read budget data from SQLite into a DataFrame
        df_budget = pd.read_sql_query(query_budget, conn)

        # Check if the budget exists
        if df_budget.empty:
            print("No budget found for the provided budget_id.")
            return

        # Query to select expense data associated with the current budget_id
        query_expense = f"SELECT * FROM expense WHERE budget_id = {budget_id}"
        
        # Read expense data from SQLite into a DataFrame
        df_expense = pd.read_sql_query(query_expense, conn)

        # Define the export folder
        export_folder = 'exports/excel'

        # Create the export folder if it doesn't exist
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        # Write DataFrames to an Excel file
        with pd.ExcelWriter(f'{export_folder}/EXPD_{budget_id}.xlsx') as writer:
            df_budget.to_excel(writer, sheet_name='Budget', index=False)
            df_expense.to_excel(writer, sheet_name='Expense', index=False)

        messagebox.showinfo('Budget Exported', 'Budget has been successfully Exported as Excel File.')

        # Close connection to the database
        conn.close()

    # def editBudName(self):
    #     budget_id = self.getBudgetID()
        
    #     dialog = CTkInputDialog(text="Type the New Budget Name:", title="Edit Budget Name", font=('Kameron', 20, 'bold'))
    #     newName = dialog.get_input()

    #     if newName == '':
    #         messagebox.showerror('Invalid Input', 'Please enter a Valid Name')

    #     try:
    #         conn = sqlite3.connect(DATABASE)
    #         cursor = conn.cursor()

    #         update_query = """
    #         UPDATE budget
    #         SET budget_name = ?
    #         WHERE budget_id = ?;
    #         """
    #         values = (newName, budget_id, )
    #         cursor.execute(update_query, values)

    #         conn.commit()
    #         messagebox.showinfo("Budget Name Updated", f"Budget Name updated to {newName}")

    #         # Update the displayed email in the GUI
    #         self.nameLabel.configure(text=newName)

    #     except sqlite3.Error as e:
    #         messagebox.showerror("SQLite Error", f"{e}")

    #     finally:
    #         if conn:
    #             conn.close()


if __name__ == '__main__':
    win = Win()
    win.mainloop()