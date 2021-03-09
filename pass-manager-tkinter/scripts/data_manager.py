import pandas
import os


class DataManager:

    def __init__(self):
        pass

    def get_master_details(self):
        if 'PY_PASS_MGR_USER' in os.environ and 'PY_PASS_MGR_PASS' in os.environ:
            username = os.environ.get('PY_PASS_MGR_USER')
            password = os.environ.get('PY_PASS_MGR_PASS')
        else:
            master_data = pandas.read_csv('data/master.csv')
            username = master_data.username[0]
            password = master_data.password[0]
        return username, password

    def get_saved_password_tags(self):
        password_data = pandas.read_csv('data/passwords.csv')
        tag_list = []
        for tags in password_data.tag:
            tag_list.append(str(tags).title())
        tag_list = list(set(tag_list))
        return tag_list

    def add_new_password(self, tag, user, password):
        data_to_add = [[tag, user, password]]
        new_password_data = pandas.DataFrame(data=data_to_add)
        with open('data/passwords.csv', 'a') as f:
            f.write('\n')
        new_password_data.to_csv('data/passwords.csv', mode='a', header=False, index=False)

    def get_all_passwords(self, tag):
        password_data = pandas.read_csv('data/passwords.csv')
        usernames = []
        passwords = []
        count = 0
        for this_tuple in password_data.itertuples():
            if str(this_tuple[1]) == str(tag):
                count += 1
                usernames.append(this_tuple[2])
                passwords.append(this_tuple[3])
        return count, usernames, passwords
