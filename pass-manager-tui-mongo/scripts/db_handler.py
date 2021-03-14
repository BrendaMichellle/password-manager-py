from pymongo import *
from rich.console import Console
import configparser
import time


class DbHandler:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('data/config.ini')
        self.host = config['MONGO']['host']
        self.port = config['MONGO']['port']
        self.admin_mongo_client = MongoClient('localhost:27017')
        self.current_user_client = None

    def _spinner(function):
        # Create a spinner for UI
        def wrapper(self, *args, **kwargs):
            console_obj = Console()
            with console_obj.status("Loading..."):
                return function(self, *args, **kwargs)

        return wrapper

    @_spinner
    def create_db_and_user(self, user='', password='', db_name=''):
        time.sleep(2)
        if db_name in self.admin_mongo_client.list_database_names():
            # If db already exists, a new user cannot be created.
            return False
        else:
            # Else create the db (init it) and add the user with permissions to it.
            pass_db = self.admin_mongo_client[db_name]
            pass_col = pass_db['passwords']
            pass_col.insert_one({'init': 'This is to init the db!'})
            self.admin_mongo_client[db_name].add_user(user, password, roles=[{'role': 'readWrite', 'db': db_name}])
            return True

    @_spinner
    def login(self, user='', password='', db_name=''):
        time.sleep(2)
        try:
            self.current_user_client = MongoClient(f'{self.host}:{self.port}',
                                                   username=user,
                                                   password=password,
                                                   authSource=db_name)
            if db_name in self.current_user_client.list_database_names():
                # If this user does not have data in the db then login should fail!
                return True
            else:
                return False
        except:
            return False
