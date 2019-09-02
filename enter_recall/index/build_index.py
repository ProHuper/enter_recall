from collections import defaultdict
from pyhanlp import *
import json
import re

# fetch from
# ITEM_SOURCE_JSON = '/home/huper/wordplace/virtual/81890/data/update/sqlserver/item.json'
# TYPE_SOURCE_JSON = '/home/huper/wordplace/virtual/81890/data/update/sqlserver/type.json'
ITEM_SOURCE_JSON = '../../data/update/sqlserver/item.json'
TYPE_SOURCE_JSON = '../../data/update/sqlserver/type.json'

# save to
# ITEM_INDEX_JSON = '/home/huper/wordplace/virtual/81890/data/sqlserver/itemIndex.json'
# TYPE_INDEX_JSON = '/home/huper/wordplace/virtual/81890/data/sqlserver/typeIndex.json'
# WORD_INDEX_JSON = '/home/huper/wordplace/virtual/81890/data/sqlserver/wordIndex.json'

ITEM_INDEX_JSON = '../../data/sqlserver/itemIndex.json'
TYPE_INDEX_JSON = '../../data/sqlserver/typeIndex.json'
WORD_INDEX_JSON = '../../data/sqlserver/wordIndex.json'

ITEM_DICT = defaultdict(list)  # reverse index made from enterprise service info
TYPE_DICT = defaultdict(str)
WORD_DICT = defaultdict(str)

split_pattern = r'[。＼,、，;；:：.\s+\\|]'


# format of the reverse index:
# service type -> [
#                   [enter_name, enter_address, enter_phone],
#                   [enter_name, enter_address, enter_phone],
#                   ...
#                 ]


def make_index():
    with open(ITEM_INDEX_JSON, 'w', encoding='utf8') as item_index_file, \
            open(ITEM_SOURCE_JSON, 'r', encoding='utf8') as item_file:

        # process item json file
        item_js = json.load(item_file)
        all_info = item_js['RECORDS']
        for item in all_info:
            service_title = item['TITLE']
            service_title = re.sub(u"（.*?）", "", service_title)
            service_title = re.sub(u"'.*?'", "", service_title)
            service_title = re.sub(u"‘.*?’", "", service_title)
            service_title = re.sub(u"“.*?”", "", service_title)
            service_title = re.sub(u'".*?"', "", service_title)
            service_title = re.sub(u"\\(.*?\\)", "", service_title)
            service_title = re.sub(u"（.*?\\)", "", service_title)
            service_title = re.sub(u"\\(.*?）", "", service_title)
            service_title = re.sub(u"[(（）)%]", "", service_title)
            service_title = re.sub(r'\d+|[元月年日次]|小时|起步|专业|—|-|－', '', service_title)

            res = re.split(split_pattern, service_title.strip('\n').strip(' '))
            res = list(filter(lambda x: len(x) > 1, res))
            for sub in res:
                ITEM_DICT[sub].append({'enter': item['ENTERPRISE_ID'], 'org_id': item['ORG_ID']})
        js_info = json.dumps(ITEM_DICT)
        item_index_file.write(js_info)

    with open(TYPE_INDEX_JSON, 'w', encoding='utf8') as type_index_file, \
            open(WORD_INDEX_JSON, 'w', encoding='utf8') as word_index_file, \
            open(TYPE_SOURCE_JSON, 'r', encoding='utf8') as type_file: \

        # process type json file
        type_js = json.load(type_file)
        all_info = type_js['RECORDS']
        for item in all_info:
            TYPE_DICT[item['SERVICETYPEVALUE']] = item['CODE']
            TYPE_DICT[item['KEYWORD']] = item['CODE']
            if item['SERVICETYPEVALUE']:
                value_words = HanLP.segment(item['SERVICETYPEVALUE'])
                for word in value_words:
                    WORD_DICT[word.word] = item['CODE']
            if item['KEYWORD']:
                key_words = HanLP.segment(item['KEYWORD'])
                for word in key_words:
                    WORD_DICT[word.word] = item['CODE']
        js_info = json.dumps(TYPE_DICT)
        type_index_file.write(js_info)

        js_info = json.dumps(WORD_DICT)
        word_index_file.write(js_info)


if __name__ == '__main__':
    make_index()
