import os
import sys
import string
import random
import subprocess

import sqlite3
import smtplib
import pyotp
import qrcode

from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv
from PIL import Image, ImageTk, ImageDraw, ImageOps

import customtkinter as CTk

CTk.set_appearance_mode("System")
CTk.set_default_color_theme("dark-blue")

load_dotenv()

DATABASE = os.environ.get("DATABASE")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

class TitleFrame(CTk.CTkFrame):
    def __init__(self, master, width: int, height: int):
        super().__init__(master, width, height)

        self.title = CTk.CTkLabel(self, text='Spend Wise', width=width, height=height, font=('Kameron', 40))
        self.title.grid(row=0, column=0, padx=20, pady=10)

class SubTitleFrame(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = CTk.CTkLabel(self, text='Login', width=320, height=50, font=('Kameron', 25))
        self.title.grid(row=0, column=0, padx=20, pady=0)

class LoginFormFrame(CTk.CTkFrame):
    def __init__(self, master, width=360, height=90):
        super().__init__(master, width, height)

        self.userNameVar = StringVar()
        self.passWordVar = StringVar()

        self.showHidePassVar = IntVar()

        # Username
        self.userName = CTk.CTkLabel(self, text='Username:', fg_color='transparent', font=('Kameron', 20))
        self.userName.place(x=10, y=10)

        self.uNameEnt = CTk.CTkEntry(self, font=('Kameron', 20), width=150, textvariable=self.userNameVar)
        self.uNameEnt.place(x=130, y=10)

        # Password
        self.passWord = CTk.CTkLabel(self, text='Password:', fg_color='transparent', font=('Kameron', 20))
        self.passWord.place(x=10, y=50)

        self.passWordEnt = CTk.CTkEntry(self, font=('Kameron', 20), width=150, show='*', textvariable=self.passWordVar)
        self.passWordEnt.place(x=130, y=50)

        # Show/Hide Password Button
        self.shButton = CTk.CTkButton(self, text='Show', width=65, font=('Kameron', 20), command=self.showHidePass)
        self.shButton.place(x=290, y=50)

        self.add_placeholder(self.uNameEnt, 'Username')
        self.add_placeholder(self.passWordEnt, 'Password')

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
        entry.bind("<FocusOut>", lambda event, entry=entry, placeholder=placeholder: self.on_focus_out(event, entry, placeholder))

    def on_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.configure(text_color=('black', 'white'))

    def on_focus_out(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(text_color="gray")

    # def uidset(self):
    #     if self.uidEnt.get() == '':
    #         self.uidEnt.set('0')

    # def checkUserID(self):
    #     entered_user_id = self.userIdVar.get()

    #     if not entered_user_id:
    #         messagebox.showerror("Error", "User ID cannot be empty.")
    #         return

    #     try:
    #         entered_user_id = int(entered_user_id)
    #     except ValueError:
    #         messagebox.showerror("Error", "Invalid User ID. Please enter a valid number.")
    #         return

    #     if entered_user_id not in self.userIDint:
    #         messagebox.showerror("Error", "Invalid User ID. Please select a valid User ID.")
    #         self.uidEnt.set('0')

    # def getUserIDs(self):
    #     try:
    #         conn = sqlite3.connect(DATABASE)
    #         cursor = conn.cursor()

    #         cursor.execute('SELECT user_id FROM registration')

    #         user_ids = [row[0] for row in cursor.fetchall()]

    #         self.userIDint.extend(user_ids)
    #         self.userID = [str(x) for x in self.userIDint]
    #         self.uidEnt.configure(values=self.userID)

    #     except sqlite3.Error as e:
    #         messagebox.showerror("SQLite Error", f"{e}")

    #     finally:
    #         if conn:
    #             conn.close()

class LoginPage(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.current_user_id = StringVar()
        self.username = StringVar()

        self.title("Spend Wise Login Page")
        self.geometry("400x350+50+50")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titleF = TitleFrame(self, 320, 50)
        self.titleF.place(x=20, y=20)

        self.subtitle = SubTitleFrame(master=self)
        self.subtitle.place(x=20, y=100)

        self.LoginFrame = LoginFormFrame(master=self)
        self.LoginFrame.place(x=20, y=160)

        self.login = CTk.CTkButton(self, text='Login', width=360, font=('Kameron', 20), command=self.login)
        self.login.place(x=20, y=260)

        self.fpbutton = CTk.CTkButton(self, text='Forgot Password', width=360, font=('Kameron', 20), command=self.forgot_password)
        self.fpbutton.place(x=20, y=300)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # self.getData()

    def on_close(self):
        self.destroy()
        self.quit()

    def getData(self):
        # self.LoginFrame.uidset()
        # self.user_id = self.LoginFrame.userIdVar.get()
        self.username = self.LoginFrame.userNameVar.get()
        self.password = self.LoginFrame.passWordVar.get()

        # print(self.user_id, self.username, self.password)

    def login(self):

        self.getData()

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # print(self.user_id, self.username, self.password)

            # Assuming 'registration' table has columns 'username' and 'password'
            query = f"SELECT user_id, first_name, last_name, tfa_tog FROM registration WHERE username = ? AND password = ?;"
            cursor.execute(query, (self.username, self.password))

            user_data = cursor.fetchone()

            if self.username == "" or self.password == "":
                messagebox.showerror("Fields Empty", "Username/Password field(s) are empty. Please fill the empty field.")
            elif user_data:
                user_id, first_name, last_name, tfa_tog = user_data
                messagebox.showinfo("Login Successful", f"Welcome, {first_name} {last_name}!")

                self.current_user_id = str(user_id)

                file = open('user_id_file.txt', 'w')
                file.write(self.current_user_id)
                file.close()

                if tfa_tog == "on":
                    self.TFA(self.current_user_id)
                else:
                    subprocess.run(["python", "mainPage.py"])  
                    sys.exit()
            else:
                messagebox.showerror("Login Failed", "Invalid user ID, username, or password.")

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def forgot_password(self):

        user_id = self.current_user_id

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            query = f"SELECT user_id, sqa_tog, first_name FROM registration WHERE username=?"
            cursor.execute(query, (self.username,))
            user_data = cursor.fetchone()

            if user_data:
                user_id, sqa_tog, first_name = user_data
                # print(sqa_tog)
                self.SecurityQuestion(user_id) if sqa_tog == "on" else self.OTPVerification(user_id) if sqa_tog == "off" else None

            else:
                messagebox.showerror("User ID", "To change the password please atleast enter the USER ID.")

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def SecurityQuestion(self, userid):
        win = SecurityQuestion(userid)
        win.mainloop()

    def OTPVerification(self, userid):
        win = OTPVerification(userid)
        win.mainloop()

    def TFA(self, userid):
        win = TFA(userid)
        win.mainloop()

class SecurityQuestion(CTk.CTkToplevel):
    def __init__(self, user_id):
        super().__init__()

        self.title("Forget Password Page - Security Question")
        self.geometry("400x260+470+50")
        self.resizable(False, False)

        self.focus_force()

        self.ansVar = StringVar()
        self.user_id = user_id

        self.titleF = TitleFrame(self, 320, 50)
        self.titleF.place(x=20, y=20)

        self.titleF.title.configure(text="Security Question")

        self.que = CTk.CTkLabel(self, text=f'Question : ', font=('Kameron', 20))
        self.que.place(x=20, y=120)

        self.que_ = CTk.CTkLabel(self, text=f'----', font=('Kameron', 20), wraplength=280)
        self.que_.place(x=120, y=120)

        self.ans = CTk.CTkLabel(self, text='Answer : ', fg_color='transparent', font=('Kameron', 20))
        self.ans.place(x=20, y=180)

        self.ans_ = CTk.CTkEntry(self, font=('Kameron', 20), width=270, textvariable=self.ansVar)
        self.ans_.place(x=110, y=180)

        self.cabutton = CTk.CTkButton(self, text='Check Answer', width=360, font=('Kameron', 20), command=self.checkAns)
        self.cabutton.place(x=20, y=220)

        self.protocol("WM_DELETE_WINDOW", self.on_close)


        self.getQues(self.user_id)

    def getQues(self, userid):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            query = f"SELECT sec_que, sec_que_ans FROM registration WHERE user_id=?"
            cursor.execute(query, (userid,))
            user_data = cursor.fetchone()

            if user_data:
                sec_que, self.sec_que_ans = user_data
                self.que_.configure(text=f"{sec_que}")

            else:
                messagebox.showerror("User ID", "To change the password please atleast enter the USER ID.")

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def checkAns(self):
        if self.ansVar.get() == self.sec_que_ans:
            self.passChange(self.user_id)

    def on_close(self):
        self.destroy()
        self.quit()

    def passChange(self, userid):
        self.on_close()

        win = PassChangeWin(userid)
        win.mainloop()

class OTPVerification(CTk.CTkToplevel):
    def __init__(self, user_id):
        super().__init__()
        
        self.title("Forget Password Page - Security Question")
        self.geometry("400x240+470+50")
        self.resizable(False, False)

        self.focus_force()

        self.otpVar = StringVar()
        self.user_id = user_id

        self.titleF = TitleFrame(self, 320, 50)
        self.titleF.place(x=20, y=20)

        self.titleF.title.configure(text="OTP Verification")

        self.email = CTk.CTkLabel(self, text=f'Email : ', font=('Kameron', 20))
        self.email.place(x=20, y=120)

        self.email_ = CTk.CTkLabel(self, text=f'durgeshkavate7128@gmail.com', font=('Kameron', 20))
        self.email_.place(x=100, y=120)

        self.otp_ = CTk.CTkLabel(self, text='OTP : ', fg_color='transparent', font=('Kameron', 20))
        self.otp_.place(x=20, y=155)

        self.OTP = CTk.CTkEntry(self, font=('Kameron', 20), width=270, justify='center', textvariable=self.otpVar)
        self.OTP.place(x=110, y=155)

        self.cabutton = CTk.CTkButton(self, text='Verify OTP', width=360, font=('Kameron', 20), command=self.verifyOTP)
        self.cabutton.place(x=20, y=200)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.getEmail(self.user_id)
        self.sendOTP()

    def getEmail(self, userid):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            query = f"SELECT first_name, last_name, email FROM registration WHERE user_id=?"
            cursor.execute(query, (userid,))
            user_data = cursor.fetchone()

            if user_data:
                self.first_name, self.last_name, self.email = user_data

            else:
                messagebox.showerror("User ID", "To change the password please atleast enter the USER ID.")

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def on_close(self):
        self.destroy()
        self.quit()

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

            user = self.first_name + " " + self.last_name
            otp = self.otp
            receiver_email = self.email

            body = f"Dear {user},\n\nI hope this email finds you well. We have received a request to change the password associated with your account.\n\nTo complete this process, please use the following One-Time Password (OTP)\n\nOTP : {otp}\n\nIf you did not initiate this request, please disregard this email. Your current password remains secure, and no changes will be made.\n\nBest Regards,\nSpend-Wise Services"
            subject = "Password Change Request"
            message = f"subject:{subject}\n\n{body}"

            server.sendmail(EMAIL, receiver_email, message)

            messagebox.showinfo('OTP sent', f"OTP has been sent to following Email Address : \n\n {receiver_email}\n\nPlease enter the otp sent to change the password.")

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                server.quit()
                conn.close()

    def verifyOTP(self):

        verificationOTP = self.otp
        enteredOTP = self.otpVar.get()

        try:
            conn = sqlite3.connect(DATABASE, isolation_level=None)
            cursor = conn.cursor()

            if enteredOTP == verificationOTP:
                messagebox.showinfo("Verified", f"Your Account Has been Verified.\n\nClick Ok to Procced for changing Password.")
                self.passChange(self.user_id)

            else:
                messagebox.showerror("Invalid OTP", "The OTP you have entered is Invalid.")

            

        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")

        finally:
            if conn:
                conn.close()

    def passChange(self, user_id):
        self.on_close()

        win = PassChangeWin(user_id)
        win.mainloop()
    
class PassChangeWin(CTk.CTkToplevel):
    def __init__(self, user_id):
        super().__init__()
        
        self.title("Forget Password Page - Security Question")
        self.geometry("400x220+470+50")
        self.resizable(False, False)

        self.focus_force()

        self.titleF = TitleFrame(self, 320, 50)
        self.titleF.place(x=20, y=20)

        self.titleF.title.configure(text="Password Change")

        self.passWordVar = StringVar()
        self.cpassWordVar = StringVar()

        self.user_id = user_id

        # Password
        self.passWord = CTk.CTkLabel(self, text='New Password:', fg_color='transparent', font=('Kameron', 20))
        self.passWord.place(x=20, y=100)

        self.passWordEnt = CTk.CTkEntry(self, font=('Kameron', 20), width=150, textvariable=self.passWordVar)
        self.passWordEnt.place(x=170, y=100)

        # Confirm Password
        self.cpassWord = CTk.CTkLabel(self, text='Confirm Password:', fg_color='transparent', font=('Kameron', 20))
        self.cpassWord.place(x=20, y=140)

        self.cpassWordEnt = CTk.CTkEntry(self, font=('Kameron', 20), width=150, textvariable=self.cpassWordVar)
        self.cpassWordEnt.place(x=200, y=140)

        self.cabutton = CTk.CTkButton(self, text='Change Password', width=360, font=('Kameron', 20), command=self.ChangePassword)
        self.cabutton.place(x=20, y=180)

    def ChangePassword(self):
        if self.passWordVar.get() == self.cpassWordVar.get():
            password = self.cpassWordVar.get()
            try:
                conn = sqlite3.connect(DATABASE)
                cursor = conn.cursor()

                query = "UPDATE registration SET password = ? WHERE user_id = ?"
                cursor.execute(query, (password, self.user_id))
                conn.commit()
                messagebox.showinfo("Password Changed", f"The Password of the User ID ({self.user_id}) has been changed successfully.")
                self.on_close()

            except sqlite3.Error as e:
                messagebox.showerror("SQLite Error", f"{e}")

            finally:
                if conn:
                    conn.close()
        else:
            messagebox.showerror("Password Mismatched", "New Password & Confirm Password should be same.")

    def on_close(self):
        self.destroy()
        self.quit()

class TFA(CTk.CTkToplevel):
    def __init__(self, user_id):
        super().__init__()
        
        self.title("Forget Password Page - Security Question")
        self.geometry("410x600+470+20")
        self.resizable(False, False)

        self.focus_force()

        self.titleF = TitleFrame(self, width=310, height=50)
        self.titleF.place(x=20, y=20)

        self.titleF.title.configure(text="2-F Authentication")

        self.user_id = user_id
        self.secret_key = self.get_secret_key_from_database()

        if not self.secret_key:
            messagebox.showerror("User Not Found", "User ID not found in the database.")
            self.destroy()
            return
        
        self.totp = pyotp.TOTP(self.secret_key)

        self.label_qr_code = CTk.CTkLabel(self)
        self.label_qr_code.place(x=25, y=110)

        self.entry_otp = CTk.CTkEntry(self, font=('Kameron', 20), width=200, justify='center')
        self.entry_otp.place(x=20, y=485)

        self.button_authenticate = CTk.CTkButton(self, width=150, text="Authenticate", command=self.authenticate, font=('Kameron', 20))
        self.button_authenticate.place(x=240, y=485)

        self.display_qr_code(box_size=12, width=360, border_size=2, corner_radius=15)

    def get_secret_key_from_database(self):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT secret_key FROM registration WHERE user_id = ?', (self.user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            messagebox.showerror("SQLite Error", f"{e}")
        finally:
            if conn:
                conn.close()

    

    def display_qr_code(self, box_size, width, border_size, corner_radius):
        provisioning_uri = self.totp.provisioning_uri(name=f'User_{self.user_id}', issuer_name='SpendWiseServices')
        qr_code = qrcode.make(provisioning_uri, box_size=box_size)
        qr_code = qr_code.resize((width, width), Image.LANCZOS)  # Resize the QR code image

        # Convert QR code to RGBA format
        qr_code = qr_code.convert("RGBA")

        # Create a rounded rectangle mask
        mask = Image.new("L", qr_code.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, qr_code.width, qr_code.height), corner_radius, fill=255)

        # Add the mask to the QR code
        qr_code.putalpha(mask)

        # Add a border
        bordered_qr_code = ImageOps.expand(qr_code, border=border_size, fill="#1a1a1a")

        # Convert to ImageTk format
        img = ImageTk.PhotoImage(bordered_qr_code)

        # Configure the label with the new image
        self.label_qr_code.configure(image=img)
        self.label_qr_code.image = img

        # Remove text from the label
        self.label_qr_code.configure(text="")


    def authenticate(self):
        entered_otp = self.entry_otp.get()
        
        if self.totp.verify(entered_otp):
            messagebox.showinfo("Authentication Successful", "OTP is valid. Access granted!")
            subprocess.run(["python", "mainPage.py"])  
            
        else:
            messagebox.showerror("Authentication Failed", "Invalid OTP. Access denied.")


def run():
    if __name__ == '__main__':
        app = LoginPage()
        app.mainloop()

run()
