import json
from pyhanlp import HanLP

from enter_recall.constant import V_SET, SAVED, FIL_SET
from enter_recall.index.build_index import ITEM_INDEX_JSON, TYPE_INDEX_JSON
from enter_recall.vocab.build_vocab import PARENT_INDEX_JSON, SIMILAR_INDEX_JSON, SIMILAR_SOURCE_JSON


def init_dicts():
    with open(ITEM_INDEX_JSON, 'r', encoding='utf8') as item_index_file, \
            open(TYPE_INDEX_JSON, 'r', encoding='utf8') as type_index_file:
        item_dict = json.load(item_index_file)
        type_dict = json.load(type_index_file)
        for k in item_dict.keys():
            item_dict[k]['items'] = set(item_dict[k]['items'])
        for k in type_dict.keys():
            type_dict[k] = set(type_dict[k])
    return item_dict, type_dict


def init_vocabs():
    with open(PARENT_INDEX_JSON, 'r', encoding='utf8') as parent_index_file, \
            open(SIMILAR_INDEX_JSON, 'r', encoding='utf8') as similar_index_file, \
            open(SIMILAR_SOURCE_JSON, 'r', encoding='utf8') as similar_source_file:
        parent_dict = json.load(parent_index_file)
        similar_dict = json.load(similar_index_file)
        similar_source = json.load(similar_source_file)
    return parent_dict, (similar_dict, similar_source)


def check_match_item(keys, match_item, org, items):
    for enter_id in items.keys():
        if items[enter_id]['org_id'] == org:
            counter = 0.0
            for key in keys:
                if key[0] in items[enter_id]['items']:
                    counter += key[1]
            match_item.append((enter_id, counter))


def check_match_type(keys, match_type, types):
    for code in types.keys():
        counter = 0.0
        for key in keys:
            if key[0] in types[code]:
                counter += key[1]
        match_type.append((code, counter))


def recall_and_rank(keys, limits, org, items, types):
    match_item = []
    match_type = []
    check_match_item(keys, match_item, org, items)
    check_match_type(keys, match_type, types)
    enter_res = sorted(match_item, key=lambda x: -x[1])[0: limits]
    type_res = sorted(match_type, key=lambda x: -x[1])[1]
    return enter_res, type_res


def get_keywords(query, par_dict, sim_dic):
    _words = HanLP.segment(query)
    temp = []
    added = []
    keywords = []
    visited = set()

    for word in _words:
        _word = word.word
        nature = str(word.nature)
        if _word in SAVED:
            temp.append(_word)
        elif nature in ['vn', 'vi']:
            temp.append(_word)
        elif nature == 'v' and _word in V_SET:
            temp.append(_word)
        elif nature in ['n', 'ng', 'nh', 'nhd', 'nl', 'nm', 'nz', 'nba'] and _word not in FIL_SET and len(_word) > 1:
            temp.append(_word)
    for item in temp:
        added.append((item, 1.5))
        if item in par_dict:
            added.append((par_dict[item], 1))
        if item in sim_dic[0]:
            for sim in sim_dic[1][sim_dic[0][item]]:
                added.append((sim, 1))
    for item in added:
        if item[0] not in visited:
            keywords.append(item)
            visited.add(item)
    return keywords


def query_request(sentence, limits, org, item_dict, type_dict, par_dict, sim_dic, verbose=False):
    keywords = get_keywords(sentence, par_dict, sim_dic)
    res = recall_and_rank(keywords, limits, org, item_dict, type_dict)

    if not verbose:
        try:
            return json.dumps({
                'enterMatch': res[0],
                'codeMatch': res[1][0],
                'messageCode': 0,
                'info': '解析并匹配成功。'
            }, ensure_ascii=False)
        except ValueError:
            return json.dumps({
                'messageCode': -1,
                'info': '解析并匹配失败。'
            }, ensure_ascii=False)
    else:
        return res
