from enter_recall.index import build_index
from enter_recall.vocab import build_vocab
import enter_recall.db_utils.sqlserver as sqs

import requests
import logging

if __name__ == '__main__':
    logging.info('fetching data from mysql...')
    sqs.fetch_and_write()
    logging.info('building index...')
    build_index.make_index()
    logging.info('building vocab...')
    build_vocab.make_vocab()
    logging.info('reloading dicts...')
    # res = requests.get('http://10.74.28.4:443/api/update')
    res = requests.get('http://127.0.0.1:8000/api/update')
    logging.info('update result:', res.json())



