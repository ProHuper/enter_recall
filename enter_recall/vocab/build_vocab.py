from collections import defaultdict
from pyhanlp import HanLP
import json

# fetch from
# PARENT_SOURCE_JSON = '/home/huper/wordplace/virtual/81890/data/vocab/parent.json'
# SIMILAR_SOURCE_JSON = '/home/huper/wordplace/virtual/81890/data/vocab/similar.json'
PARENT_SOURCE_JSON = '../../data/vocab/parent.json'
SIMILAR_SOURCE_JSON = '../../data/vocab/similar.json'

# save to
# PARENT_INDEX_JSON = '/home/huper/wordplace/virtual/81890/data/vocab/parent.json'
# SIMILAR_INDEX_JSON = '/home/huper/wordplace/virtual/81890/data/vocab/similar_index.json'

PARENT_INDEX_JSON = '../../data/vocab/parent_index.json'
SIMILAR_INDEX_JSON = '../../data/vocab/similar_index.json'


def make_vocab():
    with open(PARENT_INDEX_JSON, 'w', encoding='utf8') as parent_index_file, \
            open(PARENT_SOURCE_JSON, 'r', encoding='utf8') as parent_file:
        parent_info = json.load(parent_file)
        parent_dict = {}
        for k, v in parent_info.items():
            for vv in v:
                parent_dict[vv] = k
        js_info = json.dumps(parent_dict)
        parent_index_file.write(js_info)

    with open(SIMILAR_INDEX_JSON, 'w', encoding='utf8') as similar_index_file, \
            open(SIMILAR_SOURCE_JSON, 'r', encoding='utf8') as similar_file:
        similar_info = json.load(similar_file)
        similar_dict = {}
        for index, items in enumerate(similar_info):
            for sub_item in items:
                similar_dict[sub_item] = index
        js_info = json.dumps(similar_dict)
        similar_index_file.write(js_info)


if __name__ == '__main__':
    make_vocab()
