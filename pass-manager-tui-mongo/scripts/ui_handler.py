from scripts.db_handler import DbHandler
from rich import console
from rich.prompt import Prompt

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
        console_obj = console.Console()
        self.print = console_obj.print

    def start_app(self):
        self.print(logo, style="#ffbe33")

        choice = Prompt.ask('1. Log in with username and password.\n2. Create a new user.', choices=['1', '2'])
        if choice == '1':
            # Input the credentials to log in
            username = Prompt.ask("Enter your username", default="")
            password = Prompt.ask("Enter your password", default="", password=True)
            db_name = f'{username}_password'
            done = self.db_obj.login(user=username, password=password, db_name=db_name)
            print(done)
            if not done:
                print('here')
                self.print('Login Failed!', style="red on white")
            else:
                self.print('Welcome!', style="green on white")
        elif choice == '2':
            # Input the credentials to create the user
            username = Prompt.ask("Enter your username", default="")
            password = Prompt.ask("Enter your password", default="", password=True)
            db_name = f'{username}_password'
            done = self.db_obj.create_db_and_user(user=username, password=password, db_name=db_name)
            print(done)
            if not done:
                self.print('Creating the user failed!', style="red on white")
            else:
                self.print('Welcome!', style="green on white")
