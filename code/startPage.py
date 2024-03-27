import subprocess

from customtkinter import *

class Win(CTk):
    def __init__(self):
        super().__init__()

        self.title('Budget Settings')
        self.geometry('400x170+50+50')
        self.resizable(False, False)
        self.focus_force()

        self.titleFrame = CTkFrame(self, width=370, height=50)
        self.titleFrame.place(x=15, y=15)

        self.titleWin = CTkLabel(self.titleFrame, width=350, height=50, text='Spend Wise', font=('Kameron', 25, 'bold'))
        self.titleWin.place(x=10, y=0)

        self.regBtn = CTkButton(self, text='Sign Up', font=('Kameron', 20, 'bold'), width=370, command=self.signUp)
        self.regBtn.place(x=15, y=80)

        self.loginBtn = CTkButton(self, text='Login', font=('Kameron', 20, 'bold'), width=370, command=self.login)
        self.loginBtn.place(x=15, y=120)

    def login(self):
        subprocess.run(["python", "loginPage.py"])

    def signUp(self):
        subprocess.run(["python", "registerPage.py"])



if __name__ == '__main__':
    win = Win()
    win.mainloop()