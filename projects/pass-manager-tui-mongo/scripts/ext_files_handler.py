import pandas


class ExtFilesHandler:

    def __init__(self):
        pass

    def get_passwords_from_file(self, file, type_csv):
        data = pandas.read_csv(file)
        websites_list = []
        usernames_list = []
        pass_list = []
        tags_list = []
        if type_csv == 'custom':
            websites_list = list(data.website)
            usernames_list = list(data.username)
            pass_list = list(data.password)
            tags_list = list(data.tags)
        elif type_csv == 'lastpass':
            websites_list = list(data.url)
            usernames_list = list(data.username)
            pass_list = list(data.password)
            names_list = list(data.name)
            groups_list = list(data.grouping)
            for name, group in zip(names_list, groups_list):
                name = str(name)
                group = str(name)
                print('b4=', name)
                print(group)
                if name == 'nan' or name == '\x10':
                    name = ''
                if group == 'nan' or group == '\x10':
                    group = ''
                print('aft=', name)
                print(group)
                print('togrther=', name.lower() + ' ' + group.lower())
                tags_list.append(name.lower() + ' ' + group.lower())
        return websites_list, usernames_list, pass_list, tags_list
