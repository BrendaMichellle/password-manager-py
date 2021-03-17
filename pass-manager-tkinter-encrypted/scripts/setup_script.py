from tkinter import *
from tkinter import messagebox
import os
from cryptography.fernet import Fernet

BACKGROUND_COLOUR = '#495664'
FOREGROUND_COLOUR = '#f6f7d3'
DARK_TEXT_COLOUR = '#333c4a'


class Setup:
    def __init__(self):
        self.setup_screen = None
        self.master_username_var = None
        self.master_password_var = None
        self.key = None

    def make_key(self):
        self.key = Fernet.generate_key()
        with open('data/key.key', 'wb') as key_file:
            key_file.write(self.key)

    def get_key(self):
        with open('data/key.key', 'rb') as key_file:
            self.key = key_file.read()

    def write_data_to_file(self, filename, data_to_put: str):
        self.get_key()
        filename = 'data/' + filename
        fernet_obj = Fernet(self.key)
        encrypted_data = fernet_obj.encrypt(data_to_put.encode())
        with open(filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

    def append_data_to_file(self, filename, data_to_append: str):
        self.get_key()
        fernet_obj = Fernet(self.key)
        existing_data = self.get_data_from_file(filename=filename)
        filename = 'data/' + filename
        new_data = existing_data + data_to_append
        encrypted_data = fernet_obj.encrypt(new_data.encode())
        with open(filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

    def get_data_from_file(self, filename):
        self.get_key()
        filename = 'data/' + filename
        fernet_obj = Fernet(self.key)
        with open(filename, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()
        decrypted_data = fernet_obj.decrypt(encrypted)
        return decrypted_data.decode('utf-8')

    def run_setup(self):
        self.make_key()
        if 'PY_PASS_MGR_USER' not in os.environ and 'PY_PASS_MGR_PASS' not in os.environ:
            self.get_master_creds_screen()
        self.init_pass_file()

    def get_master_creds_screen(self):
        self.setup_screen = Tk()
        self.setup_screen.title('Initial Setup')
        self.setup_screen.config(padx=60, pady=50, bg=BACKGROUND_COLOUR)
        messagebox.showinfo(title='Application Setup', message='Enter credentials to use.')
        username_label = Label(master=self.setup_screen, text='Master Username: ', bg=BACKGROUND_COLOUR,
                               fg=FOREGROUND_COLOUR,
                               pady=20)
        password_label = Label(master=self.setup_screen, text='Master Password: ', bg=BACKGROUND_COLOUR,
                               fg=FOREGROUND_COLOUR,
                               pady=20)
        self.master_username_var = StringVar()
        self.master_password_var = StringVar()
        username_entry = Entry(width=30, textvariable=self.master_username_var)
        password_entry = Entry(width=30, textvariable=self.master_password_var, show='*')
        go_btn = Button(text='Go', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, command=self.set_master_creds, pady=10)
        username_label.grid(row=0, column=0)
        username_entry.grid(row=0, column=1)
        password_label.grid(row=1, column=0)
        password_entry.grid(row=1, column=1)
        go_btn.grid(row=2, column=2)
        username_entry.focus()
        self.setup_screen.mainloop()

    def set_master_creds(self):
        username = self.master_username_var.get()
        password = self.master_password_var.get()
        if username and password:
            is_okay = messagebox.askokcancel(title='Confirm', message='Are you sure to save this?')
            if is_okay:
                self.master_username_var.set('')
                self.master_password_var.set('')
                data_to_put = f'username,password\n{username},{password}'
                self.write_data_to_file(filename='master.csv', data_to_put=data_to_put)
                self.setup_screen.destroy()
        else:
            messagebox.showerror(title='Empty field(s)?', message='Please don\'t leave any field(s) empty.')

    def init_pass_file(self):
        data_to_put = 'tag,username,password\ntemp,temp,temp'
        self.write_data_to_file(filename='passwords.csv', data_to_put=data_to_put)
