import pandas


class DataManager:

    def __init__(self):
        pass

    def get_master_details(self):
        master_data = pandas.read_csv('data/master.csv')
        return master_data.username[0], master_data.password[0]
