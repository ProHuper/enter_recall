import json
from enter_recall.recall import recall_and_rank
from enter_recall.index.build_index import TYPE_SOURCE_JSON, ITEM_SOURCE_JSON

item_dict = None
type_dict = None
parent_vocab = None
sim_vocab = None

item_source = {}
type_source = {}


def load():
    global item_dict, type_dict
    item_dict, type_dict = recall_and_rank.init_dicts()
    global sim_vocab, parent_vocab
    parent_vocab, sim_vocab = recall_and_rank.init_vocabs()
    global item_source, type_source
    with open(ITEM_SOURCE_JSON, 'r', encoding='utf8') as item_file:
        json_info = json.load(item_file)['RECORDS']
        for item in json_info:
            item_source[item['ENTERPRISE_ID']] = {'name': item['NAME'], 'title': item['TITLE']}
    with open(TYPE_SOURCE_JSON, 'r', encoding='utf8') as type_file:
        json_info = json.load(type_file)['RECORDS']
        for item in json_info:
            type_source[item['CODE']] = {'keyword': item['KEYWORD'], 'value': item['SERVICETYPEVALUE']}


def show_index():
    print('company item information\n')
    for key in item_dict.keys():
        print(key, ':')
        print(item_dict[key]['items'])
    for key in type_dict.keys():
        print(key, ':')
        print(type_dict[key])


def show_keywords(inp):
    return recall_and_rank.get_keywords(inp, parent_vocab, sim_vocab)


if __name__ == '__main__':
    load()
    while True:
        sentence = input()
        if sentence == 'index':
            show_index()
        elif sentence.startswith('--'):
            show_keywords(sentence[2:])
        else:
            res = recall_and_rank.query_request(sentence,
                                                int(100),
                                                int(2),
                                                item_dict=item_dict,
                                                type_dict=type_dict,
                                                par_dict=parent_vocab,
                                                sim_dic=sim_vocab,
                                                verbose=True)
            ids = list(map(lambda x: x[0], res[0]))
            for item in ids:
                print(f"{item_source[item]['NAME']} | {item_source[item]['TITLE']}")
            print('---------------------------------')
            code = res[1][0]
            print(f"{type_source[code]['keyword']} | {type_source[code]['value']}")

