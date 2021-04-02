from scripts.db_handler import DbHandler
from scripts.password_generator import PasswordGenerator
from scripts.ext_files_handler import ExtFilesHandler
from rich import console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
import pyperclip
import tkinter as tk
from tkinter import filedialog

logo = """______            ___  ___                                 ______      
| ___ \           |  \/  |                                 | ___ \     
| |_/ /_ _ ___ ___| .  . | __ _ _ __   __ _  __ _  ___ _ __| |_/ /   _ 
|  __/ _` / __/ __| |\/| |/ _` |  _ \ / _` |/ _` |/ _ \ |__|  __/ | | |
| | | (_| \__ \__ \ |  | | (_| | | | | (_| | (_| |  __/ |  | |  | |_| |
\_|  \__,_|___/___|_|  |_/\__,_|_| |_|\__,_|\__, |\___|_|  \_|   \__, |
                                             __/ |                __/ |
                                            |___/                |___/ """


class UiHandler:

    def __init__(self):
        self.db_obj = DbHandler()
        self.ext_obj = ExtFilesHandler()
        self.pass_obj = PasswordGenerator()
        console_obj = console.Console()
        self.print = console_obj.print
        self.db_name = ''

    def start_app(self):
        cont = True

        menu = Table(title='Main Menu', show_lines=True)
        menu.add_column('Sr. No.')
        menu.add_column('Option')
        menu.add_row('1.', 'List All Passwords')
        menu.add_row('2.', 'Search for a password')
        menu.add_row('3.', 'Generate a password')
        menu.add_row('4.', 'Add a new password')
        menu.add_row('5.', 'Update an existing password')
        menu.add_row('6.', 'Delete a password')
        menu.add_row('7.', 'Intelli Dashboard')
        menu.add_row('8.', 'Import Passwords')
        menu.add_row('9.', 'Export Passwords')
        choices = [str(x) for x in range(10)]
        choices.append('clear')
        choices.append('exit')

        while cont:
            choice = Prompt.ask('Make a choice: {ENTER for menu}\n\n', choices=choices,
                                default='0')
            if choice == '0':
                self.print(menu, style="white")
            elif choice == '1':
                self.print('Listing Passwords', style="yellow on black")
                self.list_passwords('all')
            elif choice == '2':
                self.print('Search Passwords', style="yellow on black")
                self.list_passwords('search')
            elif choice == '3':
                self.print('Generate a Password', style="yellow on black")
                self.generate_password()
            elif choice == '4':
                self.print('Add a new Password', style="yellow on black")
                self.add_password()
            elif choice == '5':
                self.print('Update an existing Password', style="yellow on black")
                self.update_password()
            elif choice == '6':
                self.print('Delete an existing Password', style="yellow on black")
                self.delete_password()
            elif choice == '7':
                pass
            elif choice == '8':
                self.print('Import passwords from a file!', style="yellow on black")
                self.import_passwords()
            elif choice == '9':
                pass
            elif choice == 'exit':
                cont = False
            elif choice == 'clear':
                self.print('\n' * 10)

    def login_client(self):
        """A function to display login panel and get user credentials to use"""
        self.print(logo, style="#ffbe33")
        choice = Prompt.ask('1. Log in with username and password.\n2. Create a new user.', choices=['1', '2'])
        if choice == '1':
            # Input the credentials to log in
            username = Prompt.ask("Enter your username", default="")
            password = Prompt.ask("Enter your password", default="", password=True)
            self.db_name = f'{username}_password'
            done = self.db_obj.login(user=username, password=password, db_name=self.db_name)
            if not done:
                self.print('Login Failed!', style="red on white")
            else:
                self.print('Login Success [green]:heavy_check_mark:', style="green on white")
                self.start_app()
        elif choice == '2':
            # Input the credentials to create the user
            username = Prompt.ask("Enter your username", default="")
            password = Prompt.ask("Enter your password", default="", password=True)
            self.db_name = f'{username}_password'
            done = self.db_obj.create_db_and_user(user=username, password=password, db_name=self.db_name)
            if not done:
                self.print('Creating the user failed!', style="red on white")
            else:
                self.print('User creation was successful [green]:heavy_check_mark:', style="green on white")
                self.db_obj.login(username, password, self.db_name)
                self.start_app()

    def display_passwords(self, length, pass_list, choosing=True):
        """
        Create a table and display the list of passwords
        Params:
            pass_list: A list of data objects fetched from passwords table
        """
        result_table = Table(title='Results')
        result_table.add_column('Sr. No.')
        result_table.add_column('Website')
        result_table.add_column('Username')
        result_table.add_column('Password')
        result_table.add_column('Tags')
        result_table.add_column('Last Modified')
        row_count = 0
        usernames_list = []
        passwords_list = []
        for i in range(length):
            password_data = pass_list[i]
            try:
                website = password_data['website']
                username = password_data['username']
                password = password_data['password']
                tags = ' '.join(password_data['tags'])
                date = password_data['date_set']
            except KeyError:
                continue
            else:
                row_count += 1
                usernames_list.append(username)
                passwords_list.append(password)
                result_table.add_row(str(row_count), website, username, password, tags, date)
        self.print(result_table)
        if choosing:
            choose = Prompt.ask(
                'Enter a number to copy the password data: {ENTER to skip}\n\n',
                choices=[str(x) for x in range(row_count + 1)],
                default='0',
            )

            choose = int(choose)
            if choose > 0:
                pyperclip.copy(usernames_list[choose - 1])
                self.print('Username copied! Press Enter to copy the password...')
                input()
                pyperclip.copy(passwords_list[choose - 1])
                self.print('Password copied!')

    def list_passwords(self, key):
        """
        Get the list of passwords from db based on type of search used
        Params:
            key: A string with values: 'all' OR 'search'
        """
        if key == 'all':
            len_passwords, all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=None)
            if len_passwords > 0:
                self.display_passwords(len_passwords, all_passwords)
            else:
                self.print('Nothing to show!!', style="red on white")
        elif key == 'search':
            tags = Prompt.ask("Enter the tag(s) (separate with spaces if multiple)", default="all")
            tags = tags.split(' ')
            len_passwords, all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=tags)
            if len_passwords > 0:
                self.display_passwords(len_passwords, all_passwords)
            else:
                self.print('Nothing to show!!', style="red on white")

    def generate_password(self):
        """Generate a new password based on user requirements"""
        has_symbols = Confirm.ask("Do you want it to have symbols?")
        has_letters = True  # Always have letters
        has_numbers = Confirm.ask("Do you want it to have numbers?")
        while True:
            length = IntPrompt.ask("Enter a number between [b]8[/b] and [b]128[/b]", default=32)
            if 8 <= length <= 128:
                break
        password = self.pass_obj.generate_password(has_symbols, has_letters, has_numbers, length)
        self.print(password, style="yellow on black")
        self.print('Password was generated and copied to clipboard!', style="green on white")

    def add_password(self):
        """Add a new password to the db"""
        website = Prompt.ask("Enter the website", default="www.default.com")
        username = Prompt.ask("Enter your username", default="user")
        password = Prompt.ask("Enter your password", default="password")
        tags = Prompt.ask("Enter the tag(s) (separate with spaces if multiple)",
                          default="default")
        tags = tags.split(' ')
        tags_lowered = [tag.lower() for tag in tags]
        done = self.db_obj.add_a_password(db_name=self.db_name, website=website, username=username, password=password,
                                          tags=tags_lowered)
        if not done:
            self.print('Failed to add the password!', style="red on white")
        else:
            self.print('Done!', style="green on white")

    def update_password(self):
        """Update an existing password"""
        tags = Prompt.ask("Enter the tag(s) to search for the password (separate with spaces if multiple)",
                          default="all")
        tags = tags.split(' ')
        len_passwords, all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=tags)
        if len_passwords > 0:
            ids_list = []
            for password in all_passwords:
                ids_list.append(password['_id'])
            self.display_passwords(len_passwords, all_passwords)
            choices = [str(x) for x in range(1, len(ids_list) + 1)]
            choices.append('exit')
            pass_to_update = Prompt.ask("Enter the number of password data to delete.",
                                        choices=choices,
                                        default='exit')
            if pass_to_update == 'exit':
                return
            pass_to_update = int(pass_to_update)
            pass_to_update -= 1
            website = Prompt.ask("Enter the website", default=all_passwords[pass_to_update]['website'])
            username = Prompt.ask("Enter your username", default=all_passwords[pass_to_update]['username'])
            password = Prompt.ask("Enter your password", default=all_passwords[pass_to_update]['password'])
            tags = Prompt.ask("Enter the tags (separate with spaces if multiple)",
                              default=' '.join(all_passwords[pass_to_update]['tags']))
            tags = tags.split(' ')
            tags_lowered = [tag.lower() for tag in tags]
            done = self.db_obj.update_password(db_name=self.db_name, _id=ids_list[pass_to_update], website=website,
                                               username=username,
                                               password=password,
                                               tags=tags_lowered)
            if not done:
                self.print('Failed to update the password!', style="red on white")
            else:
                self.print('Done!', style="green on white")
        else:
            self.print('Nothing to show!!', style="red on white")

    def delete_password(self):
        """Delete an existing password"""
        tags = Prompt.ask("Enter the tag(s) to search for the password (separate with spaces if multiple)",
                          default="all")
        tags = tags.split(' ')
        if tags[0] == 'all':
            tags = None
        len_passwords, all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=tags)
        if len_passwords > 0:
            ids_list = [password['_id'] for password in all_passwords]
            self.display_passwords(len_passwords, all_passwords, choosing=False)
            choices = [str(x) for x in range(1, len(ids_list) + 1)]
            choices.append('exit')
            choices.append('all')
            pass_to_delete = Prompt.ask("Enter the number of password data to delete.",
                                        choices=choices,
                                        default='exit')
            if pass_to_delete == 'all':
                flagged = False
                for ids in ids_list:
                    done = self.db_obj.delete_password(db_name=self.db_name, _id=ids)
                    if not done:
                        self.print('Failed to delete a password!', style="red on white")
                        flagged = True
                        break
                if not flagged:
                    self.print('Done!', style="green on white")
            elif pass_to_delete == 'exit':
                return
            else:
                pass_to_update = int(pass_to_delete)
                pass_to_update -= 1
                done = self.db_obj.delete_password(db_name=self.db_name, _id=ids_list[pass_to_update])
                if not done:
                    self.print('Failed to delete the password!', style="red on white")
                else:
                    self.print('Done!', style="green on white")
        else:
            self.print('Nothing to show!', style="red on white")

    def import_passwords(self):
        """Import passwords from external files"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title='Select a CSV file to import the passwords',
                                               filetypes=(("CSV Files", "*.csv"),))
        type_csv = Prompt.ask("Enter the vendor file was exported from. {Enter help for info / exit to cancel}",
                              default='custom',
                              choices=['custom', 'lastpass'])
        if type_csv.casefold() == 'help':
            message = '''
            The vendor is inquired because different vendors will have different templates for their csv files when
            they are exported.\n
            Currently, we only support:\n
            1. our own custom template\n
            2. lastpass csv template\n
            Our CUSTOM csv template is as follows:\n
            Headers:\twebsite\tusername\tpassword\twebsite\ttags\tmodified\n
            The LASTPASS csv template is as follows:\n
            Headers:\turl\tusername\tpassword\tname\tgrouping\n
            Please make sure your csv file follows the template you selected when you import it.
            '''
            self.print(message, style="yellow on black")
            self.import_passwords()
        elif type_csv.casefold() == 'exit':
            return
        else:
            websites, usernames, passwords, tags = self.ext_obj.get_passwords_from_file(
                file=file_path,
                type_csv=type_csv.casefold())
            flagged = False
            for website, username, password, tag in zip(websites, usernames, passwords, tags):
                if not self.db_obj.add_a_password(db_name=self.db_name, website=website, username=username,
                                                  password=password, tags=tag.split(' ')):
                    self.print("There was a problem importing your passwords", style="red on white")
                    flagged = True
                    break
            if not flagged:
                self.print("All passwords were imported successfully! [green]:heavy_check_mark:",
                           style="green on white")
