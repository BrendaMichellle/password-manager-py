from scripts.db_handler import DbHandler
from scripts.password_generator import PasswordGenerator
from rich import console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table

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
        self.pass_obj = PasswordGenerator()
        console_obj = console.Console()
        self.print = console_obj.print
        self.db_name = ''

    def start_app(self):
        cont = True

        menu = Table(title='Main Menu')
        menu.add_column('Sr. No.')
        menu.add_column('Option')
        menu.add_row('1.', 'List All Passwords')
        menu.add_row('2.', 'Search for a password')
        menu.add_row('3.', 'Generate a password')
        menu.add_row('4.', 'Add a new password')
        menu.add_row('5.', 'Update an existing password')
        menu.add_row('6.', 'Intelli Dashboard')
        menu.add_row('7.', 'Import Passwords')
        menu.add_row('8.', 'Export Passwords')
        menu.add_row('9.', 'Exit')

        while cont:
            self.print('Press ENTER to continue.', style="White on black")
            input()
            self.print(menu, style="white")
            choice = Prompt.ask('Make a choice:', choices=[str(x) for x in range(1, 10)])
            if choice == '1':
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
                pass
            elif choice == '7':
                pass
            elif choice == '8':
                pass
            elif choice == '9':
                cont = False

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
                self.print('Welcome!', style="green on white")
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
                self.print('Welcome!', style="green on white")
                self.db_obj.login(username, password, self.db_name)
                self.start_app()

    def display_passwords(self, pass_list):
        """
        Create a table and display the list of passwords
        Params:
            pass_list: A list of data objects fetched from passwords table
        """
        result_table = Table(title='Results')
        result_table.add_column('Sr. No.')
        result_table.add_column('Username')
        result_table.add_column('Password')
        result_table.add_column('Tags')
        result_table.add_column('Added On')
        row_count = 0
        for password_data in pass_list:
            try:
                username = password_data['username']
                password = password_data['password']
                tags = ' '.join(password_data['tags'])
                date = password_data['date_set']
            except KeyError:
                continue
            else:
                row_count += 1
                result_table.add_row(str(row_count), username, password, tags, date)
        self.print(result_table)

    def list_passwords(self, key):
        """
        Get the list of passwords from db based on type of search used
        Params:
            key: A string with values: 'all' OR 'search'
        """
        if key == 'all':
            len_passwords, all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=None)
            if len_passwords > 0:
                self.display_passwords(all_passwords)
            else:
                self.print('No passwords to show!', style="red on white")
        elif key == 'search':
            tags = Prompt.ask("Enter the tag(s) (separate with spaces if multiple)", default="default")
            tags = tags.split(' ')
            len_passwords, all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=tags)
            if len_passwords > 0:
                self.display_passwords(all_passwords)
            else:
                self.print('No passwords to show!', style="red on white")

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
        username = Prompt.ask("Enter your username", default="")
        password = Prompt.ask("Enter your password", default="")
        tags = Prompt.ask("Enter the tag(s) to search for the password (separate with spaces if multiple)",
                          default="default")
        tags = tags.split(' ')
        tags_lowered = [tag.lower() for tag in tags]
        done = self.db_obj.add_a_password(db_name=self.db_name, username=username, password=password, tags=tags_lowered)
        if not done:
            self.print('Failed to add the password!', style="red on white")
        else:
            self.print('Done!', style="green on white")

    def update_password(self):
        """Update an existing password"""
        tags = Prompt.ask("Enter the tag(s) to search for the password (separate with spaces if multiple)",
                          default="default")
        tags = tags.split(' ')
        len_passwords, all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=tags)
        if len_passwords > 0:
            ids_list = []
            for password in all_passwords:
                ids_list.append(password['_id'])
                self.print(password['_id'])
            self.display_passwords(all_passwords)
            pass_to_update = IntPrompt.ask("Enter the number of password data to edit.",
                                           choices=[str(x) for x in range(1, len(ids_list) + 1)])
            pass_to_update -= 1
            username = Prompt.ask("Enter your username", default=all_passwords[pass_to_update]['username'])
            password = Prompt.ask("Enter your password", default=all_passwords[pass_to_update]['password'])
            tags = Prompt.ask("Enter the tags (separate with spaces if multiple)",
                              default=' '.join(all_passwords[pass_to_update]['tags']))
            tags = tags.split(' ')
            tags_lowered = [tag.lower() for tag in tags]
            done = self.db_obj.update_password(db_name=self.db_name, _id=ids_list[pass_to_update], username=username,
                                               password=password,
                                               tags=tags_lowered)
            if not done:
                self.print('Failed to update the password!', style="red on white")
            else:
                self.print('Done!', style="green on white")
