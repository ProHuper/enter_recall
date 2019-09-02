import sys
import json
from pyhanlp import *
from enter_recall.vec.sim import o_sim, cos_sim
from enter_recall.build_index.build_index import ITEM_INDEX_JSON, TYPE_INDEX_JSON, WORD_INDEX_JSON

ITEM_VECTOR_PATH = '/home/huper/wordplace/virtual/81890/data/sqlserver/itemVector.json'
TYPE_VECTOR_PATH = '/home/huper/wordplace/virtual/81890/data/sqlserver/typeVector.json'
WORD_VECTOR_PATH = '/home/huper/wordplace/virtual/81890/data/sqlserver/wordVector.json'
WORD_VECTOR_TOTAL = '/home/huper/wordplace/virtual/81890/data/sqlserver/wordTotal.json'

# ITEM_VECTOR_PATH = '../../data/sqlserver/itemVector.json'
# TYPE_VECTOR_PATH = '../../data/sqlserver/typeVector.json'
# WORD_VECTOR_PATH = '../../data/sqlserver/wordVector.json'
# WORD_VECTOR_TOTAL = '../../data/sqlserver/wordTotal.json'


def init_word_total():
    with open(WORD_VECTOR_TOTAL, 'r', encoding='utf8') as word_total_file:
        word_total = json.load(word_total_file)
    return word_total


def init_dicts():
    with open(ITEM_INDEX_JSON, 'r', encoding='utf8') as item_index_file, \
            open(TYPE_INDEX_JSON, 'r', encoding='utf8') as type_index_file, \
            open(WORD_INDEX_JSON, 'r', encoding='utf8') as word_index_file:
        item_dict = json.load(item_index_file)
        type_dict = json.load(type_index_file)
        word_dict = json.load(word_index_file)
    return item_dict, type_dict, word_dict


def init_vecs():
    with open(ITEM_VECTOR_PATH, 'r', encoding='utf8') as item_vec_file, \
            open(TYPE_VECTOR_PATH, 'r', encoding='utf8') as type_vec_file, \
            open(WORD_VECTOR_PATH, 'r', encoding='utf8') as word_vec_file:
        item_vecs = json.load(item_vec_file)
        type_vecs = json.load(type_vec_file)
        word_vecs = json.load(word_vec_file)
    return item_vecs, type_vecs, word_vecs


def recall_and_rank(code, single_code,
                    limits, org,
                    item_vecs, items,
                    type_vecs, types,
                    word_vecs, words,
                    word_flag=False,
                    disFunc='cos_dis'):
    dists = []
    res = []
    res_set = set()
    func = cos_sim if disFunc == 'cos_dis' else o_sim

    for k, v in item_vecs.items():
        sim = func(code, v)
        dists.append((k, sim))
    # dists -> {item1: sim, item2: sim...}
    dists = sorted(dists, key=lambda x: -x[1])
    # 如果在这里就给dists取limit，并不是在筛选企业的数目，而是在筛选item或者type的数目，但是这两者是一对多的。

    for item in dists:
        for _ in items[item[0]]:
            # format: id/enter -> score,在这里限制企业数目。
            if _['enter'] not in res_set and _['org_id'] == org:
                res.append((_['enter'], item[1]))
                res_set.add(_['enter'])
        if len(res) >= limits:
            break
    res = res[0: limits]

    dists = []
    if word_flag:
        for k, v in word_vecs.items():
            sim = func(single_code, v)
            dists.append((k, sim))
        # dists -> {item1: sim, item2: sim...}
        dists = sorted(dists, key=lambda x: -x[1])
        return res, (words[dists[0][0]], dists[0][1])

    else:
        for k, v in type_vecs.items():
            sim = func(code, v)
            dists.append((k, sim))
        # dists -> {item1: sim, item2: sim...}
        dists = sorted(dists, key=lambda x: -x[1])
        return res, (types[dists[0][0]], dists[0][1])


def check_all_key_words(keys, codes, single_code,
                        limits, org,
                        item_vecs, items,
                        type_vecs, types,
                        word_vecs, words,
                        word_flag=False):
    # all_res = {'item': [], 'type': []}
    # final_res = {'item': [], 'type': []}
    all_res_item = []
    all_res_type = []
    for index, code in enumerate(codes):
        single_res, code_match = recall_and_rank(code, single_code,
                                                 limits, org,
                                                 item_vecs, items,
                                                 type_vecs, types,
                                                 word_vecs, words,
                                                 word_flag=word_flag)
        # ietm选企业，使用平局分或者使用最高分。
        # mean_item = 0.0
        # for enters in single_res:
        #     mean_item += enters[1]
        # try:
        #     mean_item /= len(single_res)
        # except ZeroDivisionError:
        #     mean_item = 0.0
        # 所有关键词匹配结果，格式：[(key, mean, enters), (key, mean, enters), (key, mean, enters)...]
        all_res_item.append((keys[index], single_res[0][1], single_res))
        all_res_type.append((code_match[0], code_match[1], keys[index]))
    # only return keyword match with max match point.
    max_index_item, max_point_item = 0, 0
    max_index_type, max_point_type = 0, 0
    for index, item in enumerate(all_res_item):
        if item[1] > max_point_item:
            max_index_item = index
            max_point_item = item[1]
    for index, type_ in enumerate(all_res_type):
        if type_[1] > max_point_type:
            max_index_type = index
            max_point_type = type_[1]
    final_res = (all_res_item[max_index_item], all_res_type[max_index_type])
    # 最高分关键词结果，格式：(key, mean, enter list, code list)
    return final_res


def full_process(words, keywords):
    for index in range(len(words) - 1):
        if str(words[index].nature) == 'n' and str(words[index + 1].nature) == 'nnd':
            keywords.append(words[index].word + words[index + 1].word)


def window_process(words, window_size, keywords):
    words = list(filter(lambda x: x.word != '人', words))
    for index in range(len(words) - window_size + 1):
        bag = [(index, words[index])]
        for _ in range(1, window_size):
            bag.append((index + _, words[index + _]))
        vs = []
        ns = []
        a = []
        ule = []
        for word in bag:
            if str(word[1].nature)[0] == 'n':
                ns.append((word[0], word[1].word))
            elif str(word[1].nature)[0] == 'v':
                vs.append((word[0], word[1].word))
            elif str(word[1].nature)[0] == 'a':
                a.append((word[0], word[1].word))
            elif str(word[1].nature) == 'ule':
                ule.append((word[0], word[1].word))

        for v in vs:
            for n in ns:
                if v[0] < n[0]:
                    keywords.append(v[1] + n[1])
        if ns and a and ule:
            keywords.append(ns[0][1] + a[0][1] + ule[0][1])
    return keywords


def key_word_process(query, window_size=4):
    keywords = []
    words = HanLP.segment(query)
    if len(words) == 1:
        return query
    # words = [('修', 'v'), ('下水道', 'n')]
    if len(words) <= 3:
        return [query]

    full_process(words, keywords)
    window_process(words, window_size, keywords)
    if not len(keywords):
        window_process(words, len(words), keywords)
    if not len(keywords):
        for seg in words:
            if str(seg.nature)[0] == 'n':
                keywords.append(seg.word)
    if not len(keywords):
        keywords.append(words[0].word)
    return list(set(keywords))


def get_keywords(query):
    # 使用TextRank算法提取关键词和关键短语
    keywords = HanLP.extractKeyword(query, 5)
    phrases = HanLP.extractPhrase(query, 5)

    # 保留关键词中的名词和含名词的关键短语
    noun_keywords = []
    for word in keywords:
        if str(HanLP.segment(word)[0].nature)[0] == 'n':
            noun_keywords.append(word)

    noun_phrases = []
    for phrase in phrases:
        flag = False
        for word in phrase:
            if str(HanLP.segment(word)[0].nature)[0] == 'n':
                flag = True
                break
        if flag is True:
            noun_phrases.append(phrase)

    # 将可以构成关键短语的关键词删去（即保留名词短语），合并关键词和关键短语
    del_keywords = []
    for phrase in noun_phrases:
        flag = True
        words = HanLP.segment(phrase)
        for word in words:
            if word.word not in noun_keywords:
                flag = False
                break
        if flag is True:
            for word in words:
                del_keywords.append(word.word)

    noun_keywords = list(set(noun_keywords).difference(set(del_keywords)))
    keywords = sorted(list(set(noun_keywords + noun_phrases)))
    return keywords


def update_vector_dict(client, wc, item_dict, type_dict, word_dict):
    with open(ITEM_VECTOR_PATH, 'w', encoding='utf8') as item_vec_file:
        key_list = []
        vec_dict = {}
        for k in item_dict.keys():
            key_list.append(k)
        print('querying all items...')
        code_list = client.encode(key_list)
        print('finished querying items...')
        for index, item in enumerate(code_list):
            vec_dict[key_list[index]] = list(map(lambda x: float(x), item))
        js_info = json.dumps(vec_dict)
        item_vec_file.write(js_info)
        print('write item result finished...')
    with open(TYPE_VECTOR_PATH, 'w', encoding='utf8') as type_vec_file:
        key_list = []
        vec_dict = {}
        for k in type_dict.keys():
            key_list.append(k)
        print('querying all types...')
        code_list = client.encode(key_list)
        print('finished querying types...')
        for index, item in enumerate(code_list):
            vec_dict[key_list[index]] = list(map(lambda x: float(x), item))
        js_info = json.dumps(vec_dict)
        type_vec_file.write(js_info)
        print('write type result finished...')
    with open(WORD_VECTOR_PATH, 'w', encoding='utf8') as word_vec_file:
        key_list = []
        code_list = []
        vec_dict = {}
        print('querying all words...')
        for k in word_dict.keys():
            try:
                key_list.append(k)
                code_list.append(wc[k])
            except:
                code_list.append([0.1 for _ in range(300)])
        print('finished querying words...')
        for index, item in enumerate(code_list):
            vec_dict[key_list[index]] = list(map(lambda x: float(x), item))
        js_info = json.dumps(vec_dict)
        word_vec_file.write(js_info)
        print('write type result finished...')


def query_request(sentence, limits, org,
                  item_dict, item_vec_dict,
                  type_dict, type_vec_dict,
                  word_dict, word_vec_dict,
                  bc, wc):
    flag = False
    keywords = key_word_process(sentence)
    if type(keywords) != list:
        keywords = [keywords]
        flag = True

    try:
        code_list = bc.encode(keywords)
        single_code = []
        if flag:
            if keywords[0] in wc.keys():
                single_code = wc[keywords[0]]
            else:
                flag = False
        res = check_all_key_words(
            keywords, code_list, single_code,
            limits, org,
            item_vec_dict, item_dict,
            type_vec_dict, type_dict,
            word_vec_dict, word_dict,
            word_flag=flag
        )
        return json.dumps({
            'KeyWordItem': res[0][0],
            'KeyWordType': res[1][2],
            'enterMatch': [{'enter': _[0], 'score': _[1]} for _ in res[0][2]],
            'codeMatch': res[1][0],
            'messageCode': 0,
            'info': '解析并匹配成功。'
        }, ensure_ascii=False)
    except ValueError:
        return json.dumps({
            'messageCode': -1,
            'info': '句法解析出错。'
        }, ensure_ascii=False)
