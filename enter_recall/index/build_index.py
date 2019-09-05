from collections import defaultdict
from pyhanlp import HanLP
import json
import os

from enter_recall.constant import V_SET, FIL_SET

_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
# fetch from
ITEM_SOURCE_JSON = os.path.join(_HOME, 'data/update/sqlserver/item.json')
TYPE_SOURCE_JSON = os.path.join(_HOME, 'data/update/sqlserver/type.json')

# save to
ITEM_INDEX_JSON = os.path.join(_HOME, 'data/sqlserver/itemIndex.json')
TYPE_INDEX_JSON = os.path.join(_HOME, 'data/sqlserver/typeIndex.json')

ITEM_DICT = defaultdict(dict)
TYPE_DICT = defaultdict()


def make_index():
    with open(ITEM_INDEX_JSON, 'w', encoding='utf8') as item_index_file, \
            open(ITEM_SOURCE_JSON, 'r', encoding='utf8') as item_file:

        item_js = json.load(item_file)
        all_info = item_js['RECORDS']
        for item in all_info:
            title = item['TITLE']
            ITEM_DICT[item['ENTERPRISE_ID']]['org_id'] = item['ORG_ID']
            if 'items' not in ITEM_DICT[item['ENTERPRISE_ID']]:
                ITEM_DICT[item['ENTERPRISE_ID']]['items'] = set()
            # TODO: segment and filter here.
            segs = HanLP.segment(title)
            for word in segs:
                _word = word.word
                nature = str(word.nature)
                if nature in ['vn', 'vi']:
                    ITEM_DICT[item['ENTERPRISE_ID']]['items'].add(_word)
                elif nature == 'v' and _word in V_SET:
                    ITEM_DICT[item['ENTERPRISE_ID']]['items'].add(_word)
                elif nature in ['n', 'ng', 'nh', 'nhd', 'nl', 'nm', 'nz', 'nba'] and _word not in FIL_SET and len(_word) > 1:
                    ITEM_DICT[item['ENTERPRISE_ID']]['items'].add(_word)

        for key in ITEM_DICT.keys():
            ITEM_DICT[key]['items'] = list(ITEM_DICT[key]['items'])
        js_info = json.dumps(ITEM_DICT)
        item_index_file.write(js_info)

    with open(TYPE_INDEX_JSON, 'w', encoding='utf8') as type_index_file, \
            open(TYPE_SOURCE_JSON, 'r', encoding='utf8') as type_file:

        type_js = json.load(type_file)
        all_info = type_js['RECORDS']
        for item in filter(lambda x: len(x['CODE']) == 9, all_info):
            TYPE_DICT[item['CODE']] = set()
            if item['SERVICETYPEVALUE']:
                value_words = HanLP.segment(item['SERVICETYPEVALUE'])
                for word in value_words:
                    TYPE_DICT[item['CODE']].add(word.word)
            if item['KEYWORD']:
                key_words = HanLP.segment(item['KEYWORD'])
                for word in key_words:
                    TYPE_DICT[item['CODE']].add(word.word)
        # convert set to list
        for k in TYPE_DICT.keys():
            TYPE_DICT[k] = list(TYPE_DICT[k])

        js_info = json.dumps(TYPE_DICT)
        type_index_file.write(js_info)


if __name__ == '__main__':
    make_index()