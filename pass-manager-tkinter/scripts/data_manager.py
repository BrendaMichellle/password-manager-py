import pandas


class DataManager:

    def __init__(self):
        pass

    def get_master_details(self):
        master_data = pandas.read_csv('data/master.csv')
        return master_data.username[0], master_data.password[0]

    def get_saved_password_tags(self):
        password_data = pandas.read_csv('data/passwords.csv')
        tag_list = []
        for tags in password_data.tag:
            tag_list.append(str(tags).title())
        tag_list = list(set(tag_list))
        return tag_list
