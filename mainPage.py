# Imports

import os
import json
import subprocess

import sqlite3

from tkinter import *
from CTkScrollableDropdown import *

from PIL import Image
from dotenv import load_dotenv
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

from datetime import datetime as dt

from AddPlaceHolder import *
from CTkTable import *

import tkinter as tk
import customtkinter as CTk


# Apperance
CTk.set_appearance_mode("System")
CTk.set_default_color_theme("dark-blue")

# Environment Variables
load_dotenv()

DATABASE = os.environ.get("DATABASE")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

JSON_FILE = os.environ.get('JSON_FILE')

# Frames
class NavigationFrame(CTk.CTkFrame):
    def __init__(self, master, width: int, height: int, button_callback):
        super().__init__(master, width, height)

        # Images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        navigation_light = Image.open(os.path.join(image_path, "menu-burger_light.png"))
        navigation_dark = Image.open(os.path.join(image_path, "menu-burger_dark.png"))

        settings_light = Image.open(os.path.join(image_path, "settings_light.png"))
        settings_dark = Image.open(os.path.join(image_path, "settings_dark.png"))

        home_light = Image.open(os.path.join(image_path, "home_light.png"))
        home_dark = Image.open(os.path.join(image_path, "home_dark.png"))

        profile_light = Image.open(os.path.join(image_path, "user_light.png"))
        profile_dark = Image.open(os.path.join(image_path, "user_dark.png"))

        archive_light = Image.open(os.path.join(image_path, "archive_light.png"))
        archive_dark = Image.open(os.path.join(image_path, "archive_dark.png"))

        self.navigationImg = CTk.CTkImage(light_image=navigation_light, dark_image=navigation_dark, size=(20, 20))
        
        self.homeImg = CTk.CTkImage(light_image=home_light, dark_image=home_dark, size=(20, 20))
        self.profileImg = CTk.CTkImage(light_image=profile_light, dark_image=profile_dark, size=(20, 20))
        self.settingsImg = CTk.CTkImage(light_image=settings_light, dark_image=settings_dark, size=(20, 20))
        self.archiveImg = CTk.CTkImage(light_image=archive_light, dark_image=archive_dark, size=(20, 20))
        
        #===============================
        self.title = CTk.CTkLabel(self, text='  Navigation Menu', font=('Kameron', 22, "bold"), width=230, height=40, image=self.navigationImg, compound='left')
        self.title.place(x=10, y=0)

        self.page = 'settings'

        self.home_btn = CTk.CTkButton(self, width=230, height=40, border_spacing=10, font=('Kameron', 20,), text="  Home", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.button_pressed("home"), image=self.homeImg)
        self.home_btn.place(x=10, y=60)

        self.profile_btn = CTk.CTkButton(self, width=230, height=40, border_spacing=10, font=('Kameron', 20,), text="   Profile", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.button_pressed("profile"), image=self.profileImg)
        self.profile_btn.place(x=10, y=110)

        self.settings_btn = CTk.CTkButton(self, width=230, height=40, border_spacing=10, font=('Kameron', 20,), text="  Settings", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.button_pressed("settings"), image=self.settingsImg)
        self.settings_btn.place(x=10, y=420)

        self.archieve_btn = CTk.CTkButton(self, width=230, height=40, border_spacing=10, font=('Kameron', 20,), text="  Archived Budgets", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.button_pressed("archive"), image=self.archiveImg)
        self.archieve_btn.place(x=10, y=160)

        self.button_callback = button_callback

    def button_pressed(self, button_name):
        # Call the callback function with the pressed button name
        if self.button_callback:
            self.button_callback(button_name)

class CalculatorFrame(CTk.CTkFrame):
    def __init__(self, master, width: int, height: int):
        super().__init__(master, width, height)

        # Entry field with integrated delete button
        self.entry = CTk.CTkEntry(self, font=('Kameron', 25), justify='right', width=310, height=50)
        self.entry.place(x=10, y=10)
        self.entry.bind("<FocusIn>", self.enable_buttons)
        self.entry.bind("<FocusOut>", self.disable_buttons)
        self.entry.bind("<Return>", lambda event=None: self.on_button_click('='))

        # Buttons
        buttons = [
            ('C', 10, 80), ('()', 90, 80), ('%', 170, 80), ('/', 250, 80),
            ('7', 10, 160), ('8', 90, 160), ('9', 170, 160), ('*', 250, 160),
            ('4', 10, 240), ('5', 90, 240), ('6', 170, 240), ('-', 250, 240),
            ('1', 10, 320), ('2', 90, 320), ('3', 170, 320), ('+', 250, 320),
            ('+/-', 10, 400), ('0', 90, 400), ('.', 170, 400), ('=', 250, 400),
        ]

        button_width = 70
        button_height = 70

        self.buttons = []
        for (text, x, y) in buttons:
            button = CTk.CTkButton(self, width=button_width, height=button_height, text=text, font=('Arial', 18), command=lambda t=text: self.on_button_click(t))
            button.place(x=x, y=y)
            self.buttons.append(button)
            button['state'] = 'disabled'

        self.bracket_state = 'open'  # Initial state

    def on_button_click(self, value):
        current_text = self.entry.get()

        if value == '=':
            try:
                result = str(eval(current_text))
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, result)
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        elif value == 'C':
            self.entry.delete(0, tk.END)
        elif value == '+/-':
            if current_text and current_text[0] == '-':
                self.entry.delete(0)
            else:
                self.entry.insert(0, '-')
        elif value == '()':
            if self.bracket_state == 'open':
                self.entry.insert(tk.END, '(')
                self.bracket_state = 'close'
            else:
                self.entry.insert(tk.END, ')')
                self.bracket_state = 'open'
        else:
            self.entry.insert(tk.END, value)

    def enable_buttons(self, event):
        for button in self.buttons:
            button['state'] = 'normal'

    def disable_buttons(self, event):
        for button in self.buttons:
            button['state'] = 'disabled'

class Footer(CTk.CTkFrame):
    def __init__(self, master, width: int, height: int):
        super().__init__(master, width, height)

        footer_text = 'Contact us if any Queries\nMobile: +91 985XX XXXXX\tEmail: services.spendwise@gmail.com'

        label = CTk.CTkLabel(self, text=footer_text, font=('Kameron', 20), width = 1270, height=50)
        label.place(x=10, y=0)

# Main Frames
class HomeFrame(CTk.CTkFrame): #(680x480+285+105)
    def __init__(self, master, width: int, height: int, user_id):
        super().__init__(master, width, height)

        '''
        Bs = Budgets 
        BE = Budget & Expense
        '''

        # Frames
        self.BsFra = CTk.CTkScrollableFrame(self, 628, 100)
        self.BsFra.place(x=15, y=15)

        self.BEFra = CTk.CTkFrame(self, 650, 235)
        self.BEFra.place(x=15, y=235)

        self.addBudFrame = CTk.CTkFrame(self.BEFra, 310, 215)
        self.addBudFrame.place(x=10, y=10)

        self.addExpFrame = CTk.CTkFrame(self.BEFra, 310, 215)
        self.addExpFrame.place(x=330, y=10)

        #======================================================================================
        # Add Budget Frame

        self.budNameVar = StringVar()
        self.budAmountVar = StringVar()
        self.budCateVar = StringVar()
        # Labels
        self.budName = CTk.CTkLabel(self.addBudFrame, text='Budget Name:', font=('Kameron', 17))
        self.budName.place(x=15, y=15)

        self.budAmount = CTk.CTkLabel(self.addBudFrame, text='Budget Amount:', font=('Kameron', 17))
        self.budAmount.place(x=15, y=75)

        # Entry Fields
        self.nameEnt = CTk.CTkEntry(self.addBudFrame, width=280, font=('Kameron', 17), textvariable=self.budNameVar)
        self.nameEnt.place(x=15, y=42)

        self.amountEnt = CTk.CTkEntry(self.addBudFrame, width=280, font=('Kameron', 17), textvariable=self.budAmountVar)
        self.amountEnt.place(x=15, y=102)

        # Button
        self.addButton = CTk.CTkButton(self.addBudFrame, text='Add Budget', font=('Kameron', 17), width=280, command=(self.addBudget))
        self.addButton.place(x=15, y=175)

        EntryPlaceholderManager(self.nameEnt, 'Budget Name')
        EntryPlaceholderManager(self.amountEnt, 'Budget Amount')

        #====================================================================================
        # Add Expense Frame
        self.expNameVar = StringVar()
        self.expAmountVar = IntVar()

        self.budid = IntVar()
        self.budname = StringVar()

        self.user_id = user_id
        self.budgets = ["Select Budget"]
        self.added = False

        # Labels
        self.expName = CTk.CTkLabel(self.addExpFrame, text='Expense Name:', font=('Kameron', 17))
        self.expName.place(x=15, y=15)

        self.expAmount = CTk.CTkLabel(self.addExpFrame, text='Expense Amount:', font=('Kameron', 17))
        self.expAmount.place(x=15, y=75)

        # Entry Fields
        self.enameEnt = CTk.CTkEntry(self.addExpFrame, width=280, font=('Kameron', 17), textvariable=self.expNameVar)
        self.enameEnt.place(x=15, y=42)

        self.eamountEnt = CTk.CTkEntry(self.addExpFrame, width=280, font=('Kameron', 17), textvariable=self.expAmountVar)
        self.eamountEnt.place(x=15, y=102)

        self.budEnt = CTk.CTkComboBox(self.addExpFrame, width=280, font=('Kameron', 17))
        self.budEnt.place(x=15, y=142)

        self.sd = CTkScrollableDropdownFrame(self.budEnt, values=self.budgets, justify="left", button_color="transparent", autocomplete=True)

        # Button
        self.addButton = CTk.CTkButton(self.addExpFrame, text='Add Expense', font=('Kameron', 17), width=280, command=self.budgetCheck)
        self.addButton.place(x=15, y=175)

        EntryPlaceholderManager(self.enameEnt, 'Expense Name')

        # Funtion Calls
        self.load_budgetCards(user_id)
        self.getBudgets(user_id)

    #=================================================================================
    # Get Functions
    
    def load_budgetCards(self, user_id):
        self.user_id = user_id
        self.getBudgets(user_id)
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM registration WHERE user_id = ?", (self.user_id,))
            count = cursor.fetchone()[0]

            # print('working #1')

            if count == 0:
                messagebox.showerror("Error", "Invalid budget_id")
                # print('working #2')
                return

            cursor.execute("SELECT * FROM budget WHERE user_id=?", (self.user_id, ))
            budgets = cursor.fetchall()

            if not budgets:
                for child in self.BsFra.winfo_children():
                    # print(self.BsFra.winfo_children())
                    child.destroy()
            else:
                for child in self.BsFra.winfo_children():
                    # print(self.BsFra.winfo_children())
                    child.destroy()
                for i, budget_info in enumerate(budgets):
                    # print(budget_info)
                    if budget_info:
                        budget_id, user_id, budget_name, budget_amount, budget_category, budget_status, date, time, expense_limit, archived = budget_info
                        
                        # self.budget_card.refreshButton.configure(command=self.refresh(budget_id))
                        if archived == 'no':
                            row_num = i // 2  # Two cards per row
                            col_num = i % 2   # 0 or 1 for left or right column
                            
                            self.budget_card = self.budgetCard(self.BsFra, 305, 150, budget_amount, budget_status, budget_name, row_num, col_num, budget_id)
                            self.setBudgetStatus(self.user_id, budget_id)

                            calculation = (budget_status/budget_amount) * 100

                            self.set_budget_info(budget_id, user_id, budget_category, budget_status)
                            self.progressColors(calculation)
                    else:
                        pass  
                    
            
        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error (loadBudgetCards)", f"{e}")

        finally:
            if conn:
                conn.close()

    def set_budget_info(self, budget_id, user_id, budget_category, budget_status):
        self.budget_id = budget_id
        self.user_id = user_id
        self.budget_category = budget_category
        self.budget_status = budget_status

    def budgetCard(self, master, width: int, height: int, amount, used, name, x, y, budget_id):
        self.BudgetCard = CTk.CTkFrame(master, width, height)
        self.BudgetCard.grid(row=x, column=y, padx=5, pady=5)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        self.budget_id = IntVar()
        
        settings_light = Image.open(os.path.join(image_path, "settings_light.png"))
        settings_dark = Image.open(os.path.join(image_path, "settings_dark.png"))

        refresh_light = Image.open(os.path.join(image_path, "refresh_light.png"))
        refresh_dark = Image.open(os.path.join(image_path, "refresh_dark.png"))

        cross = Image.open(os.path.join(image_path, "cross.png"))

        self.settingsImg = CTk.CTkImage(light_image=settings_light, dark_image=settings_dark, size=(20, 20))
        self.refreshImg = CTk.CTkImage(light_image=refresh_light, dark_image=refresh_dark, size=(20, 20))
        self.crossImg = CTk.CTkImage(light_image=cross, dark_image=cross, size=(20, 20))

        calculation = (int(used)/int(amount)) * 100
        unformateed_percentage = round(calculation, 2)
        percentage = self.add_zero(unformateed_percentage)

        progress = round(unformateed_percentage / 100, 2)

        self.progressVar = IntVar()
        self.toplevel_window = None

        self.name = CTk.CTkLabel(self.BudgetCard, text=name, font=('Kameron', 17))
        self.name.place(x=10, y=10)

        self.amount = CTk.CTkLabel(self.BudgetCard, text=f"Alloted: ${'{:,}'.format(amount)}", font=('Kameron', 17))
        self.amount.place(x=10, y=35)
        
        self.used = CTk.CTkLabel(self.BudgetCard, text=f"Used: ${'{:,}'.format(used)}", font=('Kameron', 17))
        self.used.place(x=10, y=60)
        
        self.status = CTk.CTkLabel(self.BudgetCard, text=f"{percentage}%", font=('Kameron', 17))
        self.status.place(x=230, y=60)

        self.progress = CTk.CTkProgressBar(self.BudgetCard, height=12, width=285, variable=self.progressVar)
        self.progress.place(x=10, y=90)

        self.progress.set(progress)

        self.settingsButton = CTk.CTkButton(self.BudgetCard, text="", image=self.settingsImg, width=20, height=20, fg_color="transparent", hover_color=("gray70", "gray30"), border_width=1, command=lambda budget_id=budget_id: self.settings(budget_id))
        self.settingsButton.place(x=180, y=10)

        self.refreshButton = CTk.CTkButton(self.BudgetCard, text="", image=self.refreshImg, width=20, height=20, fg_color="transparent", hover_color=("gray70", "gray30"), border_width=1, command=lambda budget_id=budget_id: self.refresh(budget_id))
        self.refreshButton.place(x=220, y=10)

        self.deleteButton = CTk.CTkButton(self.BudgetCard, text="", image=self.crossImg, width=20, height=20, fg_color="transparent", hover_color=("gray70", "#6a0000"), border_width=1, border_color='#FF0000', command=lambda budget_id=budget_id: self.deleteBudget(budget_id))
        self.deleteButton.place(x=260, y=10)

        self.viewExpenseBtn = CTk.CTkButton(self.BudgetCard, text="View Expenses" , width=285, height=25, font=('Kameron', 17, 'bold'), command=lambda id=budget_id: self.fetchExpenses(id))
        self.viewExpenseBtn.place(x=10, y=110)

    def getBudgets(self, userid):
        self.budgets = ["Select Budget"]
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            user_id = userid

            cursor.execute("SELECT archived, budget_id, budget_name FROM budget WHERE user_id = ?", (user_id,))
            budgets = cursor.fetchall()

            for tuple_item in budgets:
                archived = tuple_item[0]
                name = tuple_item[2]
                # print(name)
                if archived == 'no':
                    self.budgets.append(name)
                    self.sd.configure(values=self.budgets)

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def setBudgetStatus(self, user_id, budget_id):
        try:
            # db_lock.acquire()
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT budget_amount FROM budget WHERE budget_id=?", (budget_id,))
            budget_amount_tuple = cursor.fetchone()
            budget_amount_value = int(budget_amount_tuple[0]) if budget_amount_tuple else None

            cursor.execute("SELECT SUM(expense_amount) FROM expense WHERE budget_id=?", (budget_id,))
            total_expenses_tuple = cursor.fetchone()
            total_expenses_value = int(total_expenses_tuple[0]) if total_expenses_tuple and total_expenses_tuple[0] else 0

            if budget_amount_value is not None:
                self.used_budget = total_expenses_value
                
                updateQuery = "UPDATE budget SET budget_status=? WHERE budget_id=?"
                cursor.execute(updateQuery, (self.used_budget, budget_id))
                conn.commit()

                # self.used.configure(text = f'Used: ${self.used_budget}')

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error (setBudgetStatus)", f"{e}")

        finally:
            # db_lock.release()
            if conn:
                conn.close()

    def getSelectedBudget(self, user_id):
        selected_budget_name = self.budEnt.get()

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            if selected_budget_name != 'Select Budget':
                cursor.execute("SELECT budget_id, budget_name FROM budget WHERE user_id = ?", (user_id,))
                budgets = cursor.fetchall()

                for tuple_item in budgets:
                    name = tuple_item[1]
                    if name == selected_budget_name:
                        budget_id = tuple_item[0]
                        return selected_budget_name, budget_id
            else:
                messagebox.showerror('Budget Not Select', 'Please select a budget to add a expense in it.')
            
        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()
    
    def budgetCheck(self):
        budget = self.getSelectedBudget(self.user_id)

        if budget is not None and isinstance(budget, tuple) and len(budget) == 2:
            budname, budid = budget

            self.budid = budid
            self.budname = budname

            # print(self.budid, self.budname)

        name = self.expNameVar.get()
        amount = self.expAmountVar.get()
        explimit = 0
        

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Get Used Budget
            cursor.execute("SELECT budget_amount, budget_status, expense_limit FROM budget WHERE budget_id = ?", (self.budid,))
            result = cursor.fetchone()

            if result:
                budamount, used, limit = result

                self.leftBudget = budamount - used
                explimit = limit

            if budamount == used:
                messagebox.showerror('Budget Not Avialable', 'Your Alloted Budget Amount has been Finished. Your cannot add any more expenses in it. If you want to add more expenses please increase your budget limit in the budget settings.')
            elif amount > explimit:
                messagebox.showerror('Expense Limit Exceded', 'Your are Exceeding your one time expense limit.')
            elif amount > self.leftBudget:
                messagebox.showerror('Budget Not Available', 'Your are Exceeding your budget limit.')
            else:
                if amount < self.leftBudget:
                    self.addExpense(self.budid, name, amount)
                elif amount == self.leftBudget:
                    veri = messagebox.askyesnocancel('Budget Limit', 'If you add this expense your budget will be over are you sure you want to add this budget.')
                    if veri == True:
                        self.addExpense(self.budid, name, amount)


        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()
   
    def checkIDExists(self, id_to_check):
        conn = sqlite3.connect('spendwise.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM budget WHERE budget_id = ?", (id_to_check,))
        count = cursor.fetchone()[0]

        conn.close()

        return count > 0

    def progressColors(self, budget_used):
        if budget_used < 60 or budget_used == 60:
            self.progress.configure(progress_color='#1f538d')
            # print('<60%')
        elif budget_used > 60 and budget_used < 90:
            self.progress.configure(progress_color='#8d801f')
            # print('60% - 90%')
        else:
            self.progress.configure(progress_color='#8d1f1f')
            # print('>90%')

    # Add Functions
    def addBudget(self):
        user_id = self.user_id
        name = self.budNameVar.get()
        amount = self.budAmountVar.get()
        used = 0

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            now = dt.now()

            date = now.strftime(str(now.day) + '/' + str(now.month) + '/' + str(now.year))
            time = now.strftime(str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))

            values = (user_id, name, amount, used, date, time, amount)

            if name == 'Budget Name':
                name = ''

            if amount == 'Budget Amount':
                amount = ''

            if name != '' and amount != '':
                cursor.execute(""" INSERT INTO budget (user_id, budget_name, budget_amount, budget_status, date, time, expense_limit) VALUES (?, ?, ?, ?, ?, ?, ?) """, values)
                conn.commit()

                messagebox.showinfo('Budget Added', f'Budget Name: {name}\nAmount: ${amount}\n Budget has been added successfully.')
                self.load_budgetCards(user_id)
                self.getBudgets(user_id)
                self.clearBudgetFields()
            else:
                messagebox.showerror('Fields Empty', 'Make sur that you have entered the budget name & budget amount. You can later change the amount & name in the budget settings.')

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def addExpense(self, budget_id, name, amount):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()


            now = dt.now()

            date = now.strftime(str(now.day) + '/' + str(now.month) + '/' + str(now.year))
            time = now.strftime(str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))

            values = (budget_id, name, amount, date, time)

            if name != '' and amount != 0 and name != 'Expense Name':
            
                if self.checkIDExists(budget_id):
                    cursor.execute(""" INSERT INTO expense (budget_id, expense_name, expense_amount, date, time) VALUES (?, ?, ?, ?, ?) """, values)
                    conn.commit()

                    messagebox.showinfo('Expense Added', f'Expense of ${amount} has been added to {self.budname}')
                    self.clearExpenseFields()
                    self.refresh(budget_id) 

            else:
                messagebox.showerror('Fields Empty', 'Please enter the name and amount of the expense.')


        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    # Delete Functions
    def deleteBudget(self, budget_id):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            veri = messagebox.askyesno('Delete Budget', 'Are you sure you want to delete this budget?')

            if veri:
                cursor.execute("DELETE FROM budget WHERE budget_id=?", (budget_id,))
                conn.commit()

                messagebox.showinfo('Budget Deleted', 'The budget has been deleted successfully.')
                
        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()
        
        self.load_budgetCards(self.user_id)
        self.getBudgets(self.user_id)

    # Budget Card Functions
    def refresh(self, budget_id):
        self.setBudgetStatus(self.user_id, budget_id)
        self.load_budgetCards(self.user_id)
    
    # Clear Functions
    def clearBudgetFields(self):
        self.budNameVar.set('')
        self.budAmountVar.set('')

        EntryPlaceholderManager(self.nameEnt, 'Budget Name')
        EntryPlaceholderManager(self.amountEnt, 'Budget Amount')

    def clearExpenseFields(self):
        self.expNameVar.set('')
        EntryPlaceholderManager(self.enameEnt, 'Expense Name')

        self.expAmountVar.set(0)
        self.budEnt.set("Select Budget")

    # View Functions
    def fetchExpenses(self, budgetid):
        #__init__
        self.veToplevel = CTk.CTk()
        self.veToplevel.geometry('510x315+20+20')
        self.veToplevel.title("View Expenses")
        self.veToplevel.resizable(False, False)
        self.veToplevel.focus_force()

        # print(budgetid)

        self.frame = CTk.CTkFrame(master=self.veToplevel,
                                                      corner_radius=15,
                                                      height=260,
                                                      width=470)
        self.frame.grid(pady=15, padx=15, sticky="nws")

        columns = ('srno', 'expense_name', 'expense_amount')

        self.table = ttk.Treeview(self.frame, columns=columns, selectmode='browse', show='headings')

        self.table.heading('#1', text='Sr. No.', anchor='center')
        self.table.heading('#2', text='Expense Name', anchor='center')
        self.table.heading('#3', text='Expense Amount ($)', anchor='center')

        self.table.column('#1', width=50, anchor='center')
        self.table.column('#2', width=250, anchor='center')  
        self.table.column('#3', width=160, anchor='center')
        # print(self.table.winfo_class())

        self.table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)


        style = ttk.Style(self.table)
        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=('Kameron', 12))
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief='flat',
                        font=('Kameron', 13))
        style.map("Treeview.Heading",
                    background=[('active', '#3484F0')])

        #Table Headings
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM budget WHERE budget_id = ?", (budgetid,))
            count = cursor.fetchone()[0]

            if count == 0:
                messagebox.showerror("Error", "Invalid budget_id")
                return

            for row in self.table.get_children():
                self.table.delete(row)

            budget_id = budgetid

            cursor.execute("SELECT expense_name, expense_amount, expense_category FROM expense WHERE budget_id = ?", (budget_id,))
            expenses = cursor.fetchall()

            for i, expense in enumerate(expenses, start=1):
                expense_name, expense_amount, expense_category = expense
                if not expense_category:
                    expense_category = "N/A"

                self.table.insert('', 'end', values=(str(i), expense_name, expense_amount))

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

        self.veToplevel.mainloop()

    def add_zero(self, number):
        if len(str(number).split('.')[0]) == 1:
            return "0" + str(number)
        else:
            return str(number)

    def settings(self, budget_id):
        with open(JSON_FILE, 'r') as file:
                    data = json.load(file)
            
        data['budget_id'] = budget_id
        
        with open(JSON_FILE, 'w') as file:
            json.dump(data, file)

        result = subprocess.run(["python", "sysWin.py"])

        if result.returncode == 0:
            self.load_budgetCards(self.user_id)

class ProfileFrame(CTk.CTkFrame): #(680x480+285+105)
    def __init__(self, master, width: int, height: int):
        super().__init__(master, width, height)

        self.text = CTk.CTkLabel(self, text="profile")
        self.text.place(x=20, y=20)

class SettingsFrame(CTk.CTkFrame): #(680x480+285+105)
    def __init__(self, master, width: int, height: int):
        super().__init__(master, width, height)

        self.text = CTk.CTkLabel(self, text="settings")
        self.text.place(x=20, y=20)

class ArchiveFrame(CTk.CTkFrame): #(680x480+285+105)
    def __init__(self, master, width: int, height: int, user_id):
        super().__init__(master, width, height)

        self.load_budgetCards(user_id)

    def load_budgetCards(self, user_id):
        self.user_id = user_id
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM registration WHERE user_id = ?", (self.user_id,))
            count = cursor.fetchone()[0]

            # print('working #1')

            if count == 0:
                messagebox.showerror("Error", "Invalid budget_id")
                # print('working #2')
                return

            cursor.execute("SELECT * FROM budget WHERE user_id=?", (self.user_id, ))
            budgets = cursor.fetchall()

            if not budgets:
                for child in self.winfo_children():
                    # print(self.BsFra.winfo_children())
                    child.destroy()
            else:
                for child in self.winfo_children():
                    # print(self.BsFra.winfo_children())
                    child.destroy()
                for i, budget_info in enumerate(budgets):
                    # print(budget_info)
                    if budget_info:
                        budget_id, user_id, budget_name, budget_amount, budget_category, budget_status, date, time, expense_limit, archived = budget_info
                        
                        # self.budget_card.refreshButton.configure(command=self.refresh(budget_id))
                        if archived == 'yes':
                            row_num = i // 2  # Two cards per row
                            col_num = i % 2   # 0 or 1 for left or right column
                            
                            self.budget_card = self.budgetCard(self, 305, 150, budget_amount, budget_status, budget_name, row_num, col_num, budget_id)
                            self.setBudgetStatus(self.user_id, budget_id)

                            calculation = (budget_status/budget_amount) * 100

                            self.set_budget_info(budget_id, user_id, budget_category, budget_status)
                            self.progressColors(calculation)
                    else:
                        pass  
                    
            
        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error (loadBudgetCards)", f"{e}")

        finally:
            if conn:
                conn.close()

    def set_budget_info(self, budget_id, user_id, budget_category, budget_status):
        self.budget_id = budget_id
        self.user_id = user_id
        self.budget_category = budget_category
        self.budget_status = budget_status

    def budgetCard(self, master, width: int, height: int, amount, used, name, x, y, budget_id):
        self.BudgetCard = CTk.CTkFrame(master, width, height)
        self.BudgetCard.grid(row=x, column=y, padx=17, pady=20)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        self.budget_id = IntVar()
        
        settings_light = Image.open(os.path.join(image_path, "settings_light.png"))
        settings_dark = Image.open(os.path.join(image_path, "settings_dark.png"))

        refresh_light = Image.open(os.path.join(image_path, "refresh_light.png"))
        refresh_dark = Image.open(os.path.join(image_path, "refresh_dark.png"))

        cross = Image.open(os.path.join(image_path, "cross.png"))

        self.settingsImg = CTk.CTkImage(light_image=settings_light, dark_image=settings_dark, size=(20, 20))
        self.refreshImg = CTk.CTkImage(light_image=refresh_light, dark_image=refresh_dark, size=(20, 20))
        self.crossImg = CTk.CTkImage(light_image=cross, dark_image=cross, size=(20, 20))

        calculation = (int(used)/int(amount)) * 100
        unformateed_percentage = round(calculation, 2)
        percentage = self.add_zero(unformateed_percentage)

        progress = round(unformateed_percentage / 100, 2)

        self.progressVar = IntVar()
        self.toplevel_window = None

        self.name = CTk.CTkLabel(self.BudgetCard, text=name, font=('Kameron', 17))
        self.name.place(x=10, y=10)

        self.amount = CTk.CTkLabel(self.BudgetCard, text=f"Alloted: ${'{:,}'.format(amount)}", font=('Kameron', 17))
        self.amount.place(x=10, y=35)
        
        self.used = CTk.CTkLabel(self.BudgetCard, text=f"Used: ${'{:,}'.format(used)}", font=('Kameron', 17))
        self.used.place(x=10, y=60)
        
        self.status = CTk.CTkLabel(self.BudgetCard, text=f"{percentage}%", font=('Kameron', 17))
        self.status.place(x=230, y=60)

        self.progress = CTk.CTkProgressBar(self.BudgetCard, height=12, width=285, variable=self.progressVar)
        self.progress.place(x=10, y=90)

        self.progress.set(progress)

        self.settingsButton = CTk.CTkButton(self.BudgetCard, text="", image=self.settingsImg, width=20, height=20, fg_color="transparent", hover_color=("gray70", "gray30"), border_width=1, command=lambda budget_id=budget_id: self.settings(budget_id))
        self.settingsButton.place(x=180, y=10)

        self.refreshButton = CTk.CTkButton(self.BudgetCard, text="", image=self.refreshImg, width=20, height=20, fg_color="transparent", hover_color=("gray70", "gray30"), border_width=1, command=lambda budget_id=budget_id: self.refresh(budget_id))
        self.refreshButton.place(x=220, y=10)

        self.deleteButton = CTk.CTkButton(self.BudgetCard, text="", image=self.crossImg, width=20, height=20, fg_color="transparent", hover_color=("gray70", "#6a0000"), border_width=1, border_color='#FF0000', command=lambda budget_id=budget_id: self.deleteBudget(budget_id))
        self.deleteButton.place(x=260, y=10)

        self.viewExpenseBtn = CTk.CTkButton(self.BudgetCard, text="View Expenses" , width=285, height=25, font=('Kameron', 17, 'bold'), command=lambda id=budget_id: self.fetchExpenses(id))
        self.viewExpenseBtn.place(x=10, y=110)

    def getBudgets(self, userid):
        self.budgets = ["Select Budget"]
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            user_id = userid

            cursor.execute("SELECT budget_id, budget_name FROM budget WHERE user_id = ?", (user_id,))
            budgets = cursor.fetchall()

            for tuple_item in budgets:
                name = tuple_item[1]
                # print(name)

                self.budgets.append(name)
                self.sd.configure(values=self.budgets)

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def setBudgetStatus(self, user_id, budget_id):
        try:
            # db_lock.acquire()
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT budget_amount FROM budget WHERE budget_id=?", (budget_id,))
            budget_amount_tuple = cursor.fetchone()
            budget_amount_value = int(budget_amount_tuple[0]) if budget_amount_tuple else None

            cursor.execute("SELECT SUM(expense_amount) FROM expense WHERE budget_id=?", (budget_id,))
            total_expenses_tuple = cursor.fetchone()
            total_expenses_value = int(total_expenses_tuple[0]) if total_expenses_tuple and total_expenses_tuple[0] else 0

            if budget_amount_value is not None:
                self.used_budget = total_expenses_value
                
                updateQuery = "UPDATE budget SET budget_status=? WHERE budget_id=?"
                cursor.execute(updateQuery, (self.used_budget, budget_id))
                conn.commit()

                # self.used.configure(text = f'Used: ${self.used_budget}')

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error (setBudgetStatus)", f"{e}")

        finally:
            # db_lock.release()
            if conn:
                conn.close()

   
    def checkIDExists(self, id_to_check):
        conn = sqlite3.connect('spendwise.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM budget WHERE budget_id = ?", (id_to_check,))
        count = cursor.fetchone()[0]

        conn.close()

        return count > 0

    def progressColors(self, budget_used):
        if budget_used < 60 or budget_used == 60:
            self.progress.configure(progress_color='#1f538d')
            # print('<60%')
        elif budget_used > 60 and budget_used < 90:
            self.progress.configure(progress_color='#8d801f')
            # print('60% - 90%')
        else:
            self.progress.configure(progress_color='#8d1f1f')
            # print('>90%')

    # Delete Functions
    def deleteBudget(self, budget_id):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            veri = messagebox.askyesno('Delete Budget', 'Are you sure you want to delete this budget?')

            if veri:
                cursor.execute("DELETE FROM budget WHERE budget_id=?", (budget_id,))
                conn.commit()

                messagebox.showinfo('Budget Deleted', 'The budget has been deleted successfully.')
                
        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()
        
        self.load_budgetCards(self.user_id)
        self.getBudgets(self.user_id)

    # Budget Card Functions
    def refresh(self, budget_id):
        self.setBudgetStatus(self.user_id, budget_id)
        self.load_budgetCards(self.user_id)

    # View Functions
    def fetchExpenses(self, budgetid):
        #__init__
        self.veToplevel = CTk.CTk()
        self.veToplevel.geometry('510x315+20+20')
        self.veToplevel.title("View Expenses")
        self.veToplevel.resizable(False, False)
        self.veToplevel.focus_force()

        # print(budgetid)

        self.frame = CTk.CTkFrame(master=self.veToplevel,
                                                      corner_radius=15,
                                                      height=260,
                                                      width=470)
        self.frame.grid(pady=15, padx=15, sticky="nws")

        columns = ('srno', 'expense_name', 'expense_amount')

        self.table = ttk.Treeview(self.frame, columns=columns, selectmode='browse', show='headings')

        self.table.heading('#1', text='Sr. No.', anchor='center')
        self.table.heading('#2', text='Expense Name', anchor='center')
        self.table.heading('#3', text='Expense Amount ($)', anchor='center')

        self.table.column('#1', width=50, anchor='center')
        self.table.column('#2', width=250, anchor='center')  
        self.table.column('#3', width=160, anchor='center')
        # print(self.table.winfo_class())

        self.table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)


        style = ttk.Style(self.table)
        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=('Kameron', 12))
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief='flat',
                        font=('Kameron', 13))
        style.map("Treeview.Heading",
                    background=[('active', '#3484F0')])

        #Table Headings
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM budget WHERE budget_id = ?", (budgetid,))
            count = cursor.fetchone()[0]

            if count == 0:
                messagebox.showerror("Error", "Invalid budget_id")
                return

            for row in self.table.get_children():
                self.table.delete(row)

            budget_id = budgetid

            cursor.execute("SELECT expense_name, expense_amount, expense_category FROM expense WHERE budget_id = ?", (budget_id,))
            expenses = cursor.fetchall()

            for i, expense in enumerate(expenses, start=1):
                expense_name, expense_amount, expense_category = expense
                if not expense_category:
                    expense_category = "N/A"

                self.table.insert('', 'end', values=(str(i), expense_name, expense_amount))

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

        self.veToplevel.mainloop()

    def add_zero(self, number):
        if len(str(number).split('.')[0]) == 1:
            return "0" + str(number)
        else:
            return str(number)

    def settings(self, budget_id):
        with open(JSON_FILE, 'r') as file:
                    data = json.load(file)
            
        data['budget_id'] = budget_id
        
        with open(JSON_FILE, 'w') as file:
            json.dump(data, file)

        result = subprocess.run(["python", "sysWin.py"])

        if result.returncode == 0:
            self.load_budgetCards(self.user_id)

# Main Page
class MainPage(CTk.CTk): #toplevel
    def __init__(self):
        super().__init__()

        self.title("Spend Wise Main Page")
        self.geometry(f'{1330}x{660}+10+10')
        self.resizable(False, False)

        #----------------------------------
        # Getting the USER_ID
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
    
        self.user_id = data['user_id']
        #-----------------------------------

        # Title
        titleFrame = CTk.CTkFrame(self, width=1290, height=70)
        titleFrame.place(x=20, y=20)

        self.title = CTk.CTkLabel(titleFrame, text='Spend Wise', font=('Kameron', 40), width=1250, height=70, justify='center')
        self.title.place(x=20, y=0)

        # Navigation Frame (250x480+20+105)
        self.navFrame = NavigationFrame(self, 250, 480, self.button_pressed_callback)
        self.navFrame.place(x=20, y=105)

        # Main Frames (680x480+285+105)
        self.homeFrame = HomeFrame(self, 680, 480, self.user_id)
        self.profileFrame = ProfileFrame(self, 680, 480)
        self.settingsFrame = SettingsFrame(self, 680, 480)
        self.archiveFrame = ArchiveFrame(self, 680, 480, self.user_id)

        # Calculator Frame (330+480+980+105)
        self.calcFrame = CalculatorFrame(self, 330, 480)
        self.calcFrame.place(x=980, y=105)

        # Footer (1290x50+20+600)
        self.footer = Footer(self, 1290, 50)
        self.footer.place(x=20, y=600)

        self.button_pressed_callback('home')
        

    def button_pressed_callback(self, button_name):

        homeButton = self.navFrame.home_btn
        profileButton = self.navFrame.profile_btn
        settingsButton = self.navFrame.settings_btn
        archiveButton = self.navFrame.archieve_btn

        homeButton.configure(fg_color=("gray75", "gray25") if button_name == "home" else "transparent")
        profileButton.configure(fg_color=("gray75", "gray25") if button_name == "profile" else "transparent")
        settingsButton.configure(fg_color=("gray75", "gray25") if button_name == "settings" else "transparent")
        archiveButton.configure(fg_color=("gray75", "gray25") if button_name == "archive" else "transparent")

        if button_name == "home":
            self.homeFrame.place(x=285, y=105)
            self.homeFrame.load_budgetCards(self.user_id)
        else:
            self.homeFrame.place_forget()

        if button_name == "profile":
            self.profileFrame.place(x=285, y=105)
        else:
            self.profileFrame.place_forget()

        if button_name == "settings":
            self.settingsFrame.place(x=285, y=105)
        else:
            self.settingsFrame.place_forget()

        if button_name == "archive":
            self.archiveFrame.place(x=285, y=105)
            self.archiveFrame.load_budgetCards(self.user_id)
        else:
            self.archiveFrame.place_forget()

if __name__ == '__main__':
    app = MainPage()
    app.mainloop()