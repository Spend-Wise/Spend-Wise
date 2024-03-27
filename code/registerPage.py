import re
import os
import sys
import time
import string
import random
import subprocess

import sqlite3
import smtplib
import pyotp

from typing import Callable, Union
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from dotenv import load_dotenv

from datetime import datetime as dt
import customtkinter as CTk

from loginPage import LoginPage

CTk.set_appearance_mode("System")
CTk.set_default_color_theme("dark-blue")

load_dotenv()

DATABASE = os.environ.get("DATABASE")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

# Widgets
class FloatSpinbox(CTk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = CTk.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                             command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTk.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0, justify='center',
                                  font=('Kameron', 20), state='disabled')
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTk.CTkButton(self, text="+", width=height - 6, height=height - 6,
                                        command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.configure(state='normal')
        self.entry.insert(0, "0")
        self.entry.configure(state='disabled')

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            self.entry.configure(state='normal')
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self.entry.configure(state='disabled')
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            self.entry.configure(state='normal')
            value = int(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self.entry.configure(state='disabled')
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.configure(state='normal')
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))
        self.entry.configure(state='disabled')

class CopyText(CTk.CTkFrame):
    def __init__(self, master, width: int = 150, height: int = 32):
        super().__init__(master, width=width, height=height)

        self.configure(fg_color=("gray78", "gray28"))

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.entry = CTk.CTkEntry(self, width=310, height=height - 6, border_width=0, justify='center',
                                  font=('Kameron', 20), state='disabled')
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTk.CTkButton(self, text='Copy', width=height - 6, height=height - 6, command=self.copy_text)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

    def set(self, value):
        self.entry.configure(state='normal')
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))
        self.entry.configure(state='disabled')

    def get(self):
        return self.entry.get()

    def copy_text(self):
        text_to_copy = self.entry.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(text_to_copy)
        self.master.update()

# Frames
class TitleFrame(CTk.CTkFrame):
    def __init__(self, master, width: int, height: int):
        super().__init__(master, width, height)

        self.title = CTk.CTkLabel(self, text='Spend Wise', width=width, height=height, font=('Kameron', 40))
        self.title.grid(row=0, column=0, padx=20, pady=10)

class SubTitleFrame(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = CTk.CTkLabel(self, text='Register', width=620, height=50, font=('Kameron', 25))
        self.title.grid(row=0, column=0, padx=20, pady=0)

class PassGenFrame(CTk.CTkFrame):
    def __init__(self, master, width: int, height: int):
        super().__init__(master, width, height)

        self.spinbox = FloatSpinbox(master=self, width=180, step_size=1)
        self.spinbox.place(x=20, y=20)

        self.copytext = CopyText(master=self, width=150)
        self.copytext.place(x=20, y=60)

        self.genbutton = CTk.CTkButton(self, text='Generate', width=170, font=('Kameron', 20),
                                       command=self.showPassword)
        self.genbutton.place(x=210, y=20)

        self.spinbox.set(6)

    def generatePassword(self, length):
        characters = 'ABCDEFGHIJKLMNOPQRTUVWXYZ0123456789'
        self.password = ''.join(random.choice(characters) for _ in range(length))
        return self.password

    def showPassword(self):
        length = self.spinbox.get()

        self.copytext.set(self.generatePassword(length))

class RegFormFrame(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Variables
        self.firstNameVar = StringVar()
        self.lastNameVar = StringVar()
        self.emailVar = StringVar()
        self.userNameVar = StringVar()
        self.passWordVar = StringVar()

        self.showHidePassVar = IntVar()
        self.emailVal = IntVar()

        self.sqq = StringVar()

        self.toplevel_window = None

        # First Name
        self.firstName = CTk.CTkLabel(self, text='First Name:', fg_color='transparent', font=('Kameron', 20))
        self.firstName.grid(row=0, column=0, pady=10, padx=10)

        self.fNameEnt = CTk.CTkEntry(self, placeholder_text='First Name', font=('Kameron', 20), width=200,
                                     textvariable=self.firstNameVar)
        self.fNameEnt.grid(row=0, column=1, pady=10, padx=10)

        # Last Name
        self.lastName = CTk.CTkLabel(self, text='Last Name:', fg_color='transparent', font=('Kameron', 20))
        self.lastName.grid(row=1, column=0, pady=10, padx=10)

        self.lNameEnt = CTk.CTkEntry(self, placeholder_text='Last Name', font=('Kameron', 20), width=200,
                                     textvariable=self.lastNameVar)
        self.lNameEnt.grid(row=1, column=1, pady=10, padx=10)

        # Email
        self.email = CTk.CTkLabel(self, text='Email Add:', fg_color='transparent', font=('Kameron', 20))
        self.email.grid(row=2, column=0, pady=10, padx=10)

        self.emailEnt = CTk.CTkEntry(self, placeholder_text='Email', font=('Kameron', 20), width=400,
                                     textvariable=self.emailVar)
        self.emailEnt.grid(row=2, column=1, pady=10, padx=10)

        self.Valemail = CTk.CTkLabel(self, text='✖', fg_color='red', font=('Kameron', 20), width=27, height=27,
                                     corner_radius=5, text_color='white')
        self.Valemail.place(x=580, y=115)

        # Username
        self.userName = CTk.CTkLabel(self, text='Username:', fg_color='transparent', font=('Kameron', 20))
        self.userName.grid(row=3, column=0, pady=10, padx=10)

        self.uNameEnt = CTk.CTkEntry(self, placeholder_text='Username', font=('Kameron', 20), width=200,
                                     textvariable=self.userNameVar)
        self.uNameEnt.grid(row=3, column=1, pady=10, padx=10)

        # Password
        self.passWord = CTk.CTkLabel(self, text='Password:', fg_color='transparent', font=('Kameron', 20))
        self.passWord.grid(row=4, column=0, pady=10, padx=10)

        self.passWordEnt = CTk.CTkEntry(self, placeholder_text='Password', font=('Kameron', 20), width=200, show='*',
                                        textvariable=self.passWordVar)
        self.passWordEnt.grid(row=4, column=1, pady=10, padx=10)

        # Show/Hide Button
        self.shButton = CTk.CTkButton(self, text='Show', width=100, font=('Kameron', 20), command=self.showHidePass)
        self.shButton.grid(row=4, column=3, padx=9)

        # Generate Password Button
        self.genButton = CTk.CTkButton(self, text='Generate', width=100, font=('Kameron', 20),
                                       command=self.openPassGenWin)
        self.genButton.place(x=446, y=214)

        # Adding Placeholder Text to Each Entry Field
        self.add_placeholder(self.fNameEnt, 'First Name')
        self.add_placeholder(self.lNameEnt, 'Last Name')
        self.add_placeholder(self.emailEnt, 'Email')
        self.add_placeholder(self.uNameEnt, 'Username')
        self.add_placeholder(self.passWordEnt, 'Password')

        self.emailEnt.bind("<KeyRelease>", lambda event: self.checkEmail())


    def showHidePass(self):
        currentStatus = self.showHidePassVar.get()

        # Show Password
        if currentStatus == 0:
            self.passWordEnt.configure(show='')
            self.showHidePassVar.set(1)
        # Hide Password
        else:
            self.passWordEnt.configure(show='*')
            self.showHidePassVar.set(0)

        new_text = 'Hide' if currentStatus == 0 else 'Show'
        self.shButton.configure(text=new_text)

    def add_placeholder(self, entry, placeholder=None):
        entry.configure(text_color="gray")
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, placeholder=placeholder: self.on_focus_in(event, entry, placeholder))
        entry.bind("<FocusOut>",
                   lambda event, entry=entry, placeholder=placeholder: self.on_focus_out(event, entry, placeholder))

    def on_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.configure(text_color=('black', 'white'))

    def on_focus_out(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(text_color="gray")

    def openPassGenWin(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = PassGenWin(self)
        else:
            self.toplevel_window.focus()

    def emailValidate(self, email):
        valid_domains = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'rediffmail.com']
        email_regex = rf'^[a-zA-Z0-9_.+-]+@({"|".join(valid_domains)})$'

        return bool(re.match(email_regex, email))

    def checkEmail(self):
        email = self.emailEnt.get()
        is_valid = self.emailValidate(email)

        if is_valid:
            self.Valemail.configure(text='✔', fg_color='green')
            self.emailVal.set(1)
        else:
            self.Valemail.configure(text='✖', fg_color='red')
            self.emailVal.set(0)

class SecQueFrame(CTk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTk.CTkLabel(master=self, font=('Kameron', 20), text='Security Question (Optional)', width=620,
                                  justify='center')
        self.label.place(x=20, y=5)

        self.secQue = StringVar()
        self.secQuesAns = StringVar()

        self.values = ['Select',
                       'In what city were you born?',
                       'What is the name of your favorite pet?',
                       "What is your mother's maiden name?",
                       'What high school did you attend?',
                       'What was the name of your elementary school?',
                       'What was the make of your first car?',
                       'What was your favorite food as a child?',
                       'Where did you meet your spouse?',
                       'What year was your father (or mother) born?', ]

        self.secQues = CTk.CTkOptionMenu(self, width=400, values=self.values, state='disabled', variable=self.secQue)
        self.secQues.place(x=20, y=40)

        self.secQues.set(self.values[0])

        self.ans = CTk.CTkEntry(self, font=('Kameron', 20), width=200, textvariable=self.secQuesAns, state='disabled')
        self.ans.place(x=440, y=40)

        self.add_placeholder(self.ans, 'Answer')

    def add_placeholder(self, entry, placeholder):
        entry.configure(state='normal')
        entry.configure(text_color="gray")
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, placeholder=placeholder: self.on_focus_in(event, entry, placeholder))
        entry.bind("<FocusOut>",
                   lambda event, entry=entry, placeholder=placeholder: self.on_focus_out(event, entry, placeholder))
        entry.configure(state='disabled')

    def on_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.configure(text_color=('black', 'white'))

    def on_focus_out(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(text_color="gray")

    def enable_security_widgets(self):
        self.secQues.configure(state='normal')
        self.ans.configure(state='normal')

    def disable_security_widgets(self):
        self.secQues.configure(state='disabled')
        self.ans.configure(state='disabled')

    def TwoFacAuth(self):
        messagebox.showinfo('2-Factor Authentication',
                            'If you want to enable two factor authentication, just keep in mind that everytime you login there will be 2-Factor Authentication.')

class SecurityFrame(CTk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.securityQue = StringVar(value='off')
        self.twofactorVer = StringVar(value='off')

        self.sqCheBox = CTk.CTkCheckBox(self, text='Security Question', command=self.SecurityQuestion,
                                        variable=self.securityQue, onvalue='on', offvalue='off')
        self.sqCheBox.place(x=20, y=20)

        self.tfaCheBox = CTk.CTkCheckBox(self, text='2-Factor Authentication', command=self.TFA,
                                         variable=self.twofactorVer, onvalue='on', offvalue='off')
        self.tfaCheBox.place(x=180, y=20)

        self.nextBtn = CTk.CTkButton(self, text='Next', width=200, font=('Kameron', 20))
        self.nextBtn.place(x=450, y=15)

    def SecurityQuestion(self):
        state = self.securityQue.get()
        if state == 'on':
            self.master.secQueFrame.enable_security_widgets()
        else:
            self.master.secQueFrame.disable_security_widgets()

    def TFA(self):
        state = self.twofactorVer.get()
        if state == 'on':
            self.master.secQueFrame.TwoFacAuth()
        else:
            pass

# Main Windows
class PassGenWin(CTk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Password Generator')
        self.geometry("445x235+800+50")
        self.resizable(False, False)

        # self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets", "logo-dark.png"))
        # self.wm_iconbitmap()
        # self.after(300, lambda: self.iconphoto(False, self.iconpath))

        self.titleFrame = TitleFrame(master=self, width=400, height=50)
        self.titleFrame.place(x=20, y=20)

        self.titleFrame.title.configure(text='Password Generator', width=360)

        self.passGenFrame = PassGenFrame(master=self, width=405, height=115)
        self.passGenFrame.place(x=20, y=100)

class RegisterPage(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Spend Wise Register Page")
        self.geometry(f'{700}x{580}+45+50')
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets", "logo-dark.png"))
        # self.wm_iconbitmap()
        # self.iconphoto(False, self.iconpath)

        self.toplevel_window = None
        self.user_id = IntVar()
        

        self.titleFrame = TitleFrame(master=self, width=620, height=50)
        self.titleFrame.place(x=20, y=20)

        self.subtitleFrame = SubTitleFrame(master=self)
        self.subtitleFrame.place(x=20, y=100)

        self.regFromFrame = RegFormFrame(master=self)
        self.regFromFrame.place(x=20, y=160)

        self.secQueFrame = SecQueFrame(master=self, width=660, height=80)
        self.secQueFrame.place(x=20, y=425)

        self.secFrame = SecurityFrame(master=self, width=660, height=55)
        self.secFrame.place(x=20, y=515)

        self.secFrame.nextBtn.configure(command=self.addData)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def generate_secret_key(self):
        secret_key = pyotp.random_base32()
        return secret_key

    def checkUniqueUsername(self, username):
        try:
            conn = sqlite3.connect(DATABASE, isolation_level=None)  # Set isolation_level to None for autocommit mode
            cursor = conn.cursor()

            query = "SELECT * FROM registration WHERE username = ?"
            cursor.execute(query, (username,))

            num_rows = cursor.fetchone()

            if num_rows is not None:
                return False
            else:
                return True

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")
            # print(f"SQLite error: {e}")

        finally:
            if conn:
                conn.close()

    def restrictions(self, valid_email, sqa_tog, sec_que, sec_que_ans, first_name, username, password):
        score = 0

        # Email Validation
        if valid_email == 1:
            score += 1

            # Security Question Validation
            if sqa_tog == "on":
                if sec_que == "Select" or sec_que_ans == "Answer" or not sec_que or not sec_que_ans:
                    messagebox.showerror("Invalid Security Question", "Please select a valid security question and provide an answer.")
                else:
                    score += 1

                    # Check if fields are filled
                    if first_name and username and password:
                        score += 1

                        # Check username uniqueness
                        if self.checkUniqueUsername(username):
                            score += 1

                            # Password Length Validation
                            if len(password) >= 6:
                                score += 1

                                return score == 5

                            else:
                                messagebox.showerror("Password Too Short", "The password you have entered is too short. Password must be at least 6 characters long.")
                        else:
                            messagebox.showerror('Username Not Available', 'The username you have entered is already taken. Please choose another username.')
                    else:
                        messagebox.showerror("Fields Empty", "Ensure that you have filled the following fields: \n\n1. First Name\n2. Username\n3. Password")
            else:
                # Check if fields are filled
                if first_name and username and password:
                    score += 1

                    # Check username uniqueness
                    if self.checkUniqueUsername(username):
                        score += 1

                        # Password Length Validation
                        if len(password) >= 6:
                            score += 1

                            return score == 4

                        else:
                            messagebox.showerror("Password Too Short", "The password you have entered is too short. Password must be at least 6 characters long.")
                    else:
                        messagebox.showerror('Username Not Available', 'The username you have entered is already taken. Please choose another username.')
                else:
                    messagebox.showerror("Fields Empty", "Ensure that you have filled the following fields: \n\n1. First Name\n2. Username\n3. Password")

        else:
            messagebox.showerror("Invalid Email", "The email you have entered is not valid. The supported domains are:\n\n1. gmail.com\n2. hotmail.com\n3. outlook.com\n4. yahoo.com\n5. rediffmail.com")

        # return score == 5

    def addData(self):
        self.userVeriWin = None
        
        try:
            conn = sqlite3.connect(DATABASE, isolation_level=None)  # Set isolation_level to None for autocommit mode
            cursor = conn.cursor()

            first_name = self.regFromFrame.firstNameVar.get()
            last_name = self.regFromFrame.lastNameVar.get()
            email = self.regFromFrame.emailVar.get()
            username = self.regFromFrame.userNameVar.get()
            password = self.regFromFrame.passWordVar.get()
            sec_que = self.secQueFrame.secQue.get()
            sec_que_ans = self.secQueFrame.secQuesAns.get()
            sqa_tog = self.secFrame.securityQue.get()
            tfa_tog = self.secFrame.twofactorVer.get()
            valid_email = self.regFromFrame.emailVal.get()
            
            secret_key = self.generate_secret_key()

            now = dt.now()

            date = now.strftime(str(now.day) + '/' + str(now.month) + '/' + str(now.year))
            time = now.strftime(str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))

            # print(f"Before: first_name={first_name}")
            if first_name == "First Name":
                first_name = ""
            # print(f"After: first_name={first_name}")

            if last_name == "Last Name":
                last_name = ""

            if email == "Email":
                email = ""

            if username == "Username":
                username = ""

            if password == "Password":
                password = ""

            if sqa_tog == "off":
                go = "yes"
                if sec_que == "Select":
                    sec_que = ""
                if sec_que_ans == "Answer":
                    sec_que_ans = ""

            data_to_insert = (first_name, last_name, email, username, password, sec_que, sec_que_ans, sqa_tog, tfa_tog, valid_email, secret_key, date, time)
            insert_query = """
            INSERT INTO "registration" ("first_name", "last_name", "email", "username", "password", "sec_que", "sec_que_ans", "sqa_tog", "tfa_tog", "valid_email", "secret_key", "date", "time")
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """        
               
            restrictionsPassed = self.restrictions(valid_email, sqa_tog, sec_que, sec_que_ans, first_name, username, password)
            # print(restrictionsPassed)

            if restrictionsPassed:
                cursor.execute(insert_query, data_to_insert)
                self.setToDefault()
                messagebox.showinfo("User Registered", f"Welcome, {first_name} to the Spend Wise!!!")
                self.userVeriWin = UserVerification()
                self.user_id.set(int(cursor.lastrowid))
                self.openUserVerificationWin()
                self.userVeriWin.getData(self.user_id.get())
                self.userVeriWin.user_id = int(self.user_id.get())                    

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")
            # print(f"SQLite error: {e}")

        finally:
            if conn:
                conn.close()

    def setToDefault(self):
        self.regFromFrame.firstNameVar.set("")
        self.regFromFrame.lastNameVar.set("")
        self.regFromFrame.emailVar.set("")
        self.regFromFrame.userNameVar.set("")
        self.regFromFrame.passWordVar.set("")
        self.secQueFrame.secQue.set(self.secQueFrame.values[0])
        self.secQueFrame.secQuesAns.set("")
        self.secFrame.securityQue.set("off")
        self.secFrame.twofactorVer.set("off")
        self.regFromFrame.emailVal.set(0)

        self.regFromFrame.add_placeholder(self.regFromFrame.fNameEnt, 'First Name')
        self.regFromFrame.add_placeholder(self.regFromFrame.lNameEnt, 'Last Name')
        self.regFromFrame.add_placeholder(self.regFromFrame.emailEnt, 'Email')
        self.regFromFrame.add_placeholder(self.regFromFrame.uNameEnt, 'Username')
        self.regFromFrame.add_placeholder(self.regFromFrame.passWordEnt, 'Password')


        self.regFromFrame.checkEmail()
        self.secQueFrame.disable_security_widgets()

        self.secQueFrame.add_placeholder(self.secQueFrame.ans, 'Answer')

    def openUserVerificationWin(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = self.userVeriWin
        else:
            self.toplevel_window.focus()

    def on_close(self):
        # Handle cleanup and exit the application
        # For example, destroy the main window and exit the Tkinter mainloop
        self.destroy()
        self.quit()

class UserVerification(CTk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title('User Verification')
        self.geometry("600x500+750+50")
        self.resizable(False, False) 

        self.registerPage = RegisterPage()
        self.user_id = 0

        self.otp_var = StringVar()

        self.titleFrame = TitleFrame(master=self, width=400, height=50)
        self.titleFrame.place(x=20, y=20)

        self.titleFrame.title.configure(text='User Verification', width=520)

        self.info_frame = CTk.CTkFrame(self, 560, 150)
        self.info_frame.place(x=20, y=110)

        self.laterFrame = CTk.CTkFrame(self, 560, 70)
        self.laterFrame.place(x=20, y=410)

        self.name = CTk.CTkLabel(master=self.info_frame, text="Name : ", font=('Kameron', 20))
        self.name.place(relx=0.125, y=20, anchor='center')

        self.name_ = CTk.CTkLabel(master=self.info_frame, text="----", font=('Kameron', 20, 'bold'))
        self.name_.place(relx=0.5, y=20, anchor='center')

        self.username = CTk.CTkLabel(master=self.info_frame, text="Username : ", font=('Kameron', 20))
        self.username.place(relx=0.125, y=50, anchor='center')

        self.username_ = CTk.CTkLabel(master=self.info_frame, text="----", font=('Kameron', 20, "bold"))
        self.username_.place(relx=0.5, y=50, anchor='center')

        self.email = CTk.CTkLabel(master=self.info_frame, text="Email : ", font=('Kameron', 20))
        self.email.place(relx=0.125, y=80, anchor='center')

        self.email_ = CTk.CTkLabel(master=self.info_frame, text="----", font=('Kameron', 20, 'bold'))
        self.email_.place(relx=0.5, y=80, anchor='center')

        self.edit_btn = CTk.CTkButton(master=self.info_frame, text="Edit Email Address", font=('Kameron', 20, 'bold'), width=520, command=self.edit_button)
        self.edit_btn.place(x=20, y=105)

        self.otp_frame = CTk.CTkFrame(self, 560, 110)
        self.otp_frame.place(x=20, y=280)

        self.send_otp = CTk.CTkButton(master=self.otp_frame, text="Send OTP", font=('Kameron', 20, 'bold'), width=520, command=self.sendOTP)
        self.send_otp.place(x=20, y=20)

        self.otp_entry = CTk.CTkEntry(master=self.otp_frame, width=200, font=('Kameron', 20, 'bold'), justify='center', textvariable=self.otp_var)
        self.otp_entry.place(x=20, y=60)

        self.verify = CTk.CTkButton(master=self.otp_frame, text="Verify", font=('Kameron', 20, 'bold'), width=310, command=self.verifyOTP)
        self.verify.place(x=230, y=60)

        self.later = CTk.CTkButton(master=self.laterFrame, text="Do it Later !!!", font=('Kameron', 20, 'bold'), width=520, command=self.doItLater, height=20)
        self.later.place(x=20, y=20)

    def loginPage(self, registered:bool = False):
        if registered == True:
            
            subprocess.run(["python", "loginPage.py"])
            
            self.destroy()
            self.quit()
            sys.exit()

    def edit_button(self):
        dialog = CTk.CTkInputDialog(text="Type the New Email Address :", title="Edit Email Address", font=('Kameron', 20, 'bold'))
        
        new_email = dialog.get_input()

        if new_email is None:
            return  # User canceled the input

        # Validate the new email format (you can add more validation as needed)
        valid_domains = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'rediffmail.com']
        email_regex = rf'^[a-zA-Z0-9_.+-]+@({"|".join(valid_domains)})$'
        if not re.match(email_regex, new_email):
            messagebox.showerror("Invalid Email", "The entered email is not valid.")
            return

        # Update the email in the database
        try:
            conn = sqlite3.connect(DATABASE, isolation_level=None)
            cursor = conn.cursor()

            update_query = """
            UPDATE registration
            SET email = ?
            WHERE user_id = ?;
            """
            # print(new_email, self.user_id)
            cursor.execute(update_query, (new_email, self.user_id))

            conn.commit()
            messagebox.showinfo("Email Updated", f"Email address updated to {new_email}")

            # Update the displayed email in the GUI
            self.email_.configure(text=new_email)

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def getData(self, user_id):
        try:
            conn = sqlite3.connect(DATABASE, isolation_level=None)
            cursor = conn.cursor()

            select_query = """
            SELECT first_name, last_name, email, username
            FROM registration
            WHERE user_id = ?;
            """

            cursor.execute(select_query, (user_id,))
            result = cursor.fetchone()

            if result:
                first_name, last_name, email, username = result
                # print(result)
                
                name = first_name + " " + last_name

                self.updatLabels(name, username, email)
            else:
                messagebox.showerror("User not found.", "User not found")

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def updatLabels(self, name, username, email):
        self.name_.configure(text=name)
        self.username_.configure(text=username)
        self.email_.configure(text=email)

    def generate_alphanumeric_otp(self, length=6):
        characters = string.ascii_letters.upper() + string.digits
        otp = ''.join(random.choice(characters) for _ in range(length))
        return otp

    def sendOTP(self):
        try:
            self.otp = self.generate_alphanumeric_otp()

            conn = sqlite3.connect(DATABASE, isolation_level=None)
            cursor = conn.cursor()

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL, PASSWORD)

            

            select_query = """
            SELECT first_name, last_name, email
            FROM registration
            WHERE user_id = ?;
            """


            cursor.execute(select_query, (self.user_id,))
            result = cursor.fetchone()

            if result:
                first_name, last_name, email = result
                # print(result)
                
                user = first_name + " " + last_name
                otp = self.otp
                receiver_email = email

                body = f"Dear {user},\n\nThank you for registering with our platform. To complete the account verification process, please use the following one-time password (OTP):\n\n{otp}\n\nPlease enter this OTP on the verification page to activate your account.\n\nBest Regards,\nSpend-Wise Services"
                subject = "Account Verification - One-Time Password (OTP)"
                message = f"subject:{subject}\n\n{body}"

                server.sendmail(EMAIL, receiver_email, message)

                messagebox.showinfo('OTP sent', f"OTP has been sent to following Email Address : \n\n {receiver_email}")

            else:
                messagebox.showerror("User not found.","User not found.")

            

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                server.quit()
                conn.close()

    def verifyOTP(self):

        verificationOTP = self.otp
        enteredOTP = self.otp_var.get()

        try:
            conn = sqlite3.connect(DATABASE, isolation_level=None)
            cursor = conn.cursor()

            valid_user = 1

            update_query = """
            UPDATE registration
            SET valid_user = ?
            WHERE user_id = ?;
            """

            if enteredOTP == verificationOTP:
                # print(self.user_id)
                cursor.execute(update_query, (valid_user, self.user_id))
                conn.commit()
                messagebox.showinfo("Verified", f"Your Account Has been Verified.\n\nPlease note that your USERID is : {self.user_id}. Don't forget your USERID as it is used all over the application.")
                
                self.loginPage(True)


            else:
                messagebox.showerror("Invalid OTP", "The OTP you have entered is Invalid.")

            

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def doItLater(self):
        self.loginPage(True)

if __name__ == "__main__":
    app = RegisterPage()
    app.mainloop()