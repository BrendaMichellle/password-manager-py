from pymongo import *
from rich.console import Console
import configparser
import time
from datetime import datetime


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
            with console_obj.status("Processing..."):
                time.sleep(0.5)
                return function(self, *args, **kwargs)

        return wrapper

    @_spinner
    def create_db_and_user(self, user='', password='', db_name=''):
        if db_name in self.admin_mongo_client.list_database_names():
            # If db already exists, a new user cannot be created.
            return False
        # Else create the db (init it) and add the user with permissions to it.
        pass_db = self.admin_mongo_client[db_name]
        pass_col = pass_db['passwords']
        pass_col.insert_one({'init': 'This is to init the db!'})
        self.admin_mongo_client[db_name].add_user(user, password, roles=[{'role': 'readWrite', 'db': db_name}])
        return True

    @_spinner
    def login(self, user='', password='', db_name=''):
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

    @_spinner
    def add_a_password(self, db_name='', website='', username='', password='', tags=None):
        if tags is None:
            tags = []
        date_set = datetime.today().strftime('%d-%m-%Y')
        data = {
            'website': website,
            'username': username,
            'password': password,
            'tags': tags,
            'date_set': date_set
        }
        database = self.current_user_client[db_name]
        col = database['passwords']
        try:
            col.insert_one(data)
        except:
            return False
        else:
            return True

    @_spinner
    def get_passwords(self, db_name, search_tags=None):
        if search_tags is None:
            search_tags = []
        database = self.current_user_client[db_name]
        col = database['passwords']
        if len(search_tags) == 0:
            # We have to find all the passwords
            reply = col.find({})
            return reply.count(), list(reply)
        else:
            return_list = []
            all_passwords = col.find()
            for tag in search_tags:
                for password_data in all_passwords:
                    try:
                        tags = ' '.join(password_data['tags'])
                    except KeyError:
                        continue
                    else:
                        if tags.find(tag.lower()) != -1:
                            return_list.append(password_data)
            return len(return_list), return_list

    @_spinner
    def update_password(self, db_name, _id, website='', username='', password='', tags=None):
        if tags is None:
            tags = []
        date_set = datetime.today().strftime('%d-%m-%Y')
        database = self.current_user_client[db_name]
        col = database['passwords']
        data = {
            'website': website,
            'username': username,
            'password': password,
            'tags': tags,
            'date_set': date_set
        }
        try:
            col.update({'_id': _id}, {'$set': data})
        except:
            return False
        else:
            return True

    @_spinner
    def delete_password(self, db_name, _id):
        database = self.current_user_client[db_name]
        col = database['passwords']
        try:
            col.delete_one({'_id': _id})
        except:
            return False
        else:
            return True
