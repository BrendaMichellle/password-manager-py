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
        while cont:
            print('\n' * 10)
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
            self.print(menu, style="blue on black")
            print('\n' * 10)
            choice = Prompt.ask('Make a choice:', choices=[str(x) for x in range(1, 9)])
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
                pass
            elif choice == '6':
                pass
            elif choice == '7':
                pass
            elif choice == '8':
                pass
            cont = Confirm.ask("Go again?")

    def login_client(self):
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
        result_table = Table(title='Results')
        result_table.add_column('Username')
        result_table.add_column('Password')
        result_table.add_column('Tags')
        result_table.add_column('Added On')
        for password_data in pass_list:
            try:
                username = password_data['username']
                password = password_data['password']
                tags = ' '.join(password_data['tags'])
                date = password_data['date_set']
            except KeyError:
                continue
            else:
                result_table.add_row(username, password, tags, date)
        self.print(result_table)

    def list_passwords(self, key):
        if key == 'all':
            all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=None)
            self.display_passwords(all_passwords)
        elif key == 'search':
            tags = Prompt.ask("Enter the tags (separate with spaces if multiple)", default="default")
            tags = tags.split(' ')
            all_passwords = self.db_obj.get_passwords(db_name=self.db_name, search_tags=tags)
            self.display_passwords(all_passwords)

    def generate_password(self):
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
        username = Prompt.ask("Enter your username", default="")
        password = Prompt.ask("Enter your password", default="")
        tags = Prompt.ask("Enter the tags (separate with spaces if multiple)", default="default")
        tags = tags.split(' ')
        tags_lowered = [tag.lower() for tag in tags]
        done = self.db_obj.add_a_password(db_name=self.db_name, username=username, password=password, tags=tags_lowered)
        if not done:
            self.print('Failed to add the password!', style="red on white")
        else:
            self.print('Done!', style="green on white")
