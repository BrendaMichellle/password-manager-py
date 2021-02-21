from tkinter import *
from tkinter import messagebox
from scripts import data_manager

BACKGROUND_COLOUR = '#495664'
FOREGROUND_COLOUR = '#f6f7d3'
DARK_TEXT_COLOUR = '#333c4a'


class UI:

    def __init__(self):
        self.data_manager = data_manager.DataManager()
        self.login_window = Tk()
        self.login_window.title('Login to Password Manager')
        self.login_window.config(padx=60, pady=50, bg=BACKGROUND_COLOUR)
        self.master_username = StringVar()
        self.master_password = StringVar()
        self.init_login_window()
        self.login_window.mainloop()

    def init_login_window(self):
        user_label = Label(text='Username: ', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=20)
        user_label.grid(row=0, column=0)
        user_entry = Entry(width=20, textvariable=self.master_username)
        user_entry.grid(row=0, column=1)
        pass_label = Label(text='Password: ', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=20)
        pass_label.grid(row=1, column=0)
        pass_entry = Entry(width=20, textvariable=self.master_password, show='*')
        pass_entry.grid(row=1, column=1)
        go_btn = Button(text='Go', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, command=self.login_pressed)
        go_btn.grid(row=2, column=2)

    def login_pressed(self):
        username = self.master_username.get()
        password = self.master_password.get()
        if username and password:
            self.master_username.set('')
            self.master_password.set('')
            check_username, check_password = self.data_manager.get_master_details()
            if str(check_username) == str(username):
                if str(check_password) == str(password):
                    self.create_main_window()
                else:
                    messagebox.showerror(title='Incorrect', message='Please check the password.')
            else:
                messagebox.showerror(title='Incorrect', message='Please check the username.')
        else:
            messagebox.showerror(title='Empty field(s)?', message='Please don\'t leave any field(s) empty.')

    def create_main_window(self):
        main_window = Tk()
        main_window.title('Password Manager')
        self.login_window.destroy()
