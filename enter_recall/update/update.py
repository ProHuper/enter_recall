from enter_recall.index import build_index
import enter_recall.db_utils.sqlserver as sqs
import enter_recall.core.retriver as recall
from bert_serving.client import BertClient

import datetime
import requests

if __name__ == '__main__':
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('preparing bc client...')
    bc = BertClient()
    wc = recall.init_word_total()
    sqs.fetch_and_write()
    print('making index...')
    build_index.make_index()
    item_dict, type_dict, word_dict = recall.init_dicts()
    print('making vectors...')
    recall.update_vector_dict(bc, wc, item_dict, type_dict, word_dict)
    print('requesting...')
    res = requests.get('http://10.74.28.4:443/api/update')
    print('update result:', res.json())
    print('finished...')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('-------------------------------------------------------------')



