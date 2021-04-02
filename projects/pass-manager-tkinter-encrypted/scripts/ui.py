from tkinter import *
from tkinter import messagebox
from scripts import data_manager
from scripts import password_generator
import pyperclip

BACKGROUND_COLOUR = '#495664'
FOREGROUND_COLOUR = '#f6f7d3'
DARK_TEXT_COLOUR = '#333c4a'


class UI:

    def __init__(self):
        # Init objects
        self.data_manager_obj = data_manager.DataManager()
        # Setup files if first start
        if self.data_manager_obj.is_first_start():
            self.data_manager_obj.setup_obj.run_setup()
        # Create login window if not first start
        if not self.data_manager_obj.is_first_start():
            self.login_window = Tk()
            self.login_window.title('Login to Password Manager')
            self.login_window.config(padx=60, pady=50, bg=BACKGROUND_COLOUR)
            # Master user credentials
            self.master_username = StringVar()
            self.master_password = StringVar()
            # Init other variables required
            self.main_window = None
            self.main_image = None
            self.symbols_checked = None
            self.letters_checked = None
            self.numbers_checked = None
            self.spinbox_pass_length = None
            self.add_new_tag = None
            self.add_new_username = None
            self.add_new_pass = None
            self.select_tag = None
            self.tags_option_menu = None
            self.user_listbox = None
            self.pass_listbox = None
            # Init login window objects
            self.init_login_window()
            self.login_window.mainloop()

    def init_login_window(self):
        user_label = Label(text='Username: ', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=20)
        user_label.grid(row=0, column=0)
        user_entry = Entry(width=30, textvariable=self.master_username)
        user_entry.grid(row=0, column=1)
        pass_label = Label(text='Password: ', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=20)
        pass_label.grid(row=1, column=0)
        pass_entry = Entry(width=30, textvariable=self.master_password, show='*')
        pass_entry.grid(row=1, column=1)
        go_btn = Button(text='Go', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, command=self.login_pressed, pady=10)
        go_btn.grid(row=2, column=2)
        user_entry.focus()

    def login_pressed(self):
        username = self.master_username.get()
        password = self.master_password.get()
        if username and password:
            self.master_username.set('')
            self.master_password.set('')
            check_username, check_password = self.data_manager_obj.get_master_details()
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
        self.login_window.destroy()
        self.main_window = Tk()
        self.main_window.title('Password Manager')
        self.main_window.config(padx=50, pady=50, bg=BACKGROUND_COLOUR)
        main_canvas = Canvas(width=600, height=600)
        main_canvas.config(bg=BACKGROUND_COLOUR, highlightthickness=0)
        self.main_image = PhotoImage(file='images/password-manager.png')
        main_canvas.create_image(300, 300, image=self.main_image)
        main_canvas.grid(row=0, column=1)
        tags_label = Label(text='TAG:', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=50)
        tags_label.grid(row=1, column=0)
        self.select_tag = StringVar()
        tags_list = self.data_manager_obj.get_saved_password_tags()
        self.tags_option_menu = OptionMenu(self.main_window, self.select_tag, *tags_list)
        self.select_tag.set(tags_list[0])
        self.tags_option_menu.grid(row=1, column=1)
        search_btn = Button(text='Search', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=10,
                            command=self.list_passwords_clicked)
        search_btn.grid(row=1, column=3)
        add_btn = Button(text='Add a new entry', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=10,
                         command=self.add_new_password_clicked)
        add_btn.grid(row=2, column=0)
        gen_pass_btn = Button(text='Generate Password', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=10,
                              command=self.generate_password_clicked)
        gen_pass_btn.grid(row=2, column=1)

    def list_passwords_clicked(self):
        self.create_list_pass_window(master=self.main_window)

    def create_list_pass_window(self, master):
        list_pass_window = Toplevel(master=master)
        tag_choice = str(self.select_tag.get()).lower()
        list_pass_window.title(f'List of passwords for {tag_choice}')
        list_pass_window.config(padx=50, pady=50, bg=BACKGROUND_COLOUR)
        intruct_label = Label(master=list_pass_window, text='Click on item to copy', bg=BACKGROUND_COLOUR,
                              fg=FOREGROUND_COLOUR, pady=10)
        intruct_label.grid(row=0, column=0)
        count, user_list, pass_list = self.data_manager_obj.get_all_passwords(tag_choice)
        self.user_listbox = Listbox(master=list_pass_window, height=count)
        for i in range(count):
            self.user_listbox.insert(i, user_list[i])
        self.user_listbox.grid(row=1, column=0)
        self.pass_listbox = Listbox(master=list_pass_window, height=count)
        for i in range(count):
            self.pass_listbox.insert(i, pass_list[i])
        self.pass_listbox.grid(row=1, column=1)
        self.user_listbox.bind("<<ListboxSelect>>", self.user_listbox_used)
        self.pass_listbox.bind("<<ListboxSelect>>", self.pass_listbox_used)

    def user_listbox_used(self, event):
        if self.user_listbox.curselection():
            pyperclip.copy(self.user_listbox.get(self.user_listbox.curselection()))
            messagebox.showinfo(title='Copied',
                                message='Copied this item!')

    def pass_listbox_used(self, event):
        if self.pass_listbox.curselection():
            pyperclip.copy(self.pass_listbox.get(self.pass_listbox.curselection()))
            messagebox.showinfo(title='Copied',
                                message='Copied this item!')

    def generate_password_clicked(self):
        self.create_gen_pass_window(master=self.main_window)

    def create_gen_pass_window(self, master):
        generate_pass_window = Toplevel(master=master)
        generate_pass_window.title('Generate a new password')
        generate_pass_window.config(padx=50, pady=50, bg=BACKGROUND_COLOUR)
        self.symbols_checked = IntVar()
        self.letters_checked = IntVar()
        self.numbers_checked = IntVar()
        symbols_check = Checkbutton(master=generate_pass_window, text='Symbols', variable=self.symbols_checked, pady=10)
        symbols_check.config(bg=BACKGROUND_COLOUR, highlightthickness=0)
        symbols_check.grid(row=0, column=0)
        letters_check = Checkbutton(master=generate_pass_window, text='Letters', variable=self.letters_checked, pady=10)
        letters_check.config(bg=BACKGROUND_COLOUR, highlightthickness=0)
        letters_check.grid(row=1, column=0)
        numbers_check = Checkbutton(master=generate_pass_window, text='Numbers', variable=self.numbers_checked, pady=10)
        numbers_check.config(bg=BACKGROUND_COLOUR, highlightthickness=0)
        numbers_check.grid(row=2, column=0)
        self.spinbox_pass_length = Spinbox(master=generate_pass_window, from_=8, to=128, width=5)
        self.spinbox_pass_length.grid(row=3, column=0)
        go_btn = Button(master=generate_pass_window, text='Go', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR,
                        command=self.generate_password, pady=10)
        go_btn.grid(row=4, column=1)

    def generate_password(self):
        symbols = self.symbols_checked.get()
        letters = self.letters_checked.get()
        numbers = self.numbers_checked.get()
        pass_length = self.spinbox_pass_length.get()
        password = password_generator.generate_password(has_symbols=bool(symbols),
                                                        has_letters=bool(letters),
                                                        has_numbers=bool(numbers),
                                                        pass_length=int(pass_length))
        messagebox.showinfo(title='Password Generated!',
                            message=f'Password is copied to clipboard! \nYour password is: {password}')

    def add_new_password_clicked(self):
        self.create_add_new_password_window(master=self.main_window)

    def create_add_new_password_window(self, master):
        add_new_pass_window = Toplevel(master=master)
        add_new_pass_window.title('Add a new password entry')
        add_new_pass_window.config(padx=50, pady=50, bg=BACKGROUND_COLOUR)
        tag_label = Label(master=add_new_pass_window, text='TAG: ', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR, pady=20)
        tag_label.grid(row=0, column=0)
        self.add_new_tag = StringVar()
        tag_entry = Entry(master=add_new_pass_window, width=30, textvariable=self.add_new_tag)
        tag_entry.grid(row=0, column=1)
        user_label = Label(master=add_new_pass_window, text='USERNAME: ', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR,
                           pady=20)
        user_label.grid(row=1, column=0)
        self.add_new_username = StringVar()
        user_entry = Entry(master=add_new_pass_window, width=30, textvariable=self.add_new_username)
        user_entry.grid(row=1, column=1)
        pass_label = Label(master=add_new_pass_window, text='PASSWORD: ', bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR,
                           pady=20)
        pass_label.grid(row=2, column=0)
        self.add_new_pass = StringVar()
        pass_entry = Entry(master=add_new_pass_window, width=30, textvariable=self.add_new_pass)
        pass_entry.grid(row=2, column=1)
        add_pass_btn = Button(master=add_new_pass_window, text='Add this password', bg=BACKGROUND_COLOUR,
                              fg=FOREGROUND_COLOUR, pady=10, command=self.password_add_clicked)
        add_pass_btn.grid(row=3, column=1)

    def password_add_clicked(self):
        tag_value = str(self.add_new_tag.get())
        user_value = str(self.add_new_username.get())
        pass_value = str(self.add_new_pass.get())
        if tag_value and user_value and pass_value:
            tag_value = tag_value.lower()
            is_okay = messagebox.askokcancel(title='Confirm save?',
                                             message=f'Are you sure you want to proceed with this info?\n' +
                                                     f'Tag: {tag_value}\n' +
                                                     f'Username: {user_value}\n' +
                                                     f'Password: {pass_value}')
            if is_okay:
                self.data_manager_obj.add_new_password(tag=tag_value, user=user_value, password=pass_value)
                messagebox.showinfo(title='Success!',
                                    message='The save operation was successful!')
                # Refresh tags list in the main app screen
                self.tags_option_menu['menu'].delete(0, "end")
                for string in self.data_manager_obj.get_saved_password_tags():
                    self.tags_option_menu['menu'].add_command(label=string,
                                                              command=lambda value=string: self.select_tag.set(value))
                self.add_new_tag.set('')
                self.add_new_username.set('')
                self.add_new_pass.set('')
        else:
            self.add_new_tag.set('')
            self.add_new_username.set('')
            self.add_new_pass.set('')
