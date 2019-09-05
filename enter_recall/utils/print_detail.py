from enter_recall.recall import recall_and_rank

item_dict = None
type_dict = None


def load():
    global item_dict, type_dict
    item_dict, type_dict = recall_and_rank.init_dicts()


def show_index():
    print('company item information\n')
    for key in item_dict.keys():
        print(key, ':')
        print(item_dict[key]['items'])
    for key in type_dict.keys():
        print(key, ':')
        print(type_dict[key])


if __name__ == '__main__':
    load()
    while True:
        sentence = input()
        if sentence == 'index':
            show_index()
