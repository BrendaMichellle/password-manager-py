import pandas
import os
from scripts.setup_script import Setup
import io


class DataManager:

    def __init__(self):
        self.setup_obj = Setup()

    def is_first_start(self):
        try:
            with open('data/master.csv', 'r') as file:
                data = file.read()
            with open('data/passwords.csv', 'r') as file:
                data = file.read()
        except FileNotFoundError:
            return True
        else:
            return False

    def get_master_details(self):
        if 'PY_PASS_MGR_USER' in os.environ and 'PY_PASS_MGR_PASS' in os.environ:
            username = os.environ.get('PY_PASS_MGR_USER')
            password = os.environ.get('PY_PASS_MGR_PASS')
        else:
            master_data = self.setup_obj.get_data_from_file(filename='master.csv')
            master_data = pandas.read_csv(io.StringIO(master_data))
            username = master_data.username[0]
            password = master_data.password[0]
        return username, password

    def get_saved_password_tags(self):
        passwords_data = self.setup_obj.get_data_from_file(filename='passwords.csv')
        password_data = pandas.read_csv(io.StringIO(passwords_data))
        tag_list = [str(tags).title() for tags in password_data.tag]
        tag_list = list(set(tag_list))
        return tag_list

    def add_new_password(self, tag, user, password):
        data_to_add = '\n' + tag + ',' + user + ',' + password
        self.setup_obj.append_data_to_file(filename='passwords.csv', data_to_append=data_to_add)

    def get_all_passwords(self, tag):
        passwords_data = self.setup_obj.get_data_from_file(filename='passwords.csv')
        password_data = pandas.read_csv(io.StringIO(passwords_data))
        usernames = []
        passwords = []
        count = 0
        for this_tuple in password_data.itertuples():
            if str(this_tuple[1]) == str(tag):
                count += 1
                usernames.append(this_tuple[2])
                passwords.append(this_tuple[3])
        return count, usernames, passwords
