import sys
from flask import Flask
from flask import request
import enter_recall.core.retriver as recall

import json

app = Flask(__name__)

bc = None
item_dict = None
type_dict = None
word_dict = None
item_vec_dict = None
type_vec_dict = None
word_vec_dict = None


def load():

    global wc
    wc = recall.init_word_total()

    global item_dict, type_dict, word_dict
    item_dict, type_dict, word_dict = recall.init_dicts()

    global item_vec_dict, type_vec_dict, word_vec_dict
    item_vec_dict, type_vec_dict, word_vec_dict = recall.init_vecs()


def reload():
    global item_dict, type_dict, word_dict
    item_dict, type_dict, word_dict = recall.init_dicts()

    global item_vec_dict, type_vec_dict, word_vec_dict
    item_vec_dict, type_vec_dict, word_vec_dict = recall.init_vecs()


@app.route('/api/query', methods=['GET'])
def query():
    sentence = request.args.get("sentence")
    limits = request.args.get("limits")
    org_id = request.args.get("org")
    return recall.query_request(sentence,
                                int(limits),
                                int(org_id),
                                item_dict=item_dict,
                                item_vec_dict=item_vec_dict,
                                type_dict=type_dict,
                                type_vec_dict=type_vec_dict,
                                word_dict=word_dict,
                                word_vec_dict=word_vec_dict,
                                wc=wc,
                                bc=bc)


@app.route('/api/update', methods=['GET'])
def update():
    try:
        reload()
        return json.dumps({'message': 'succeed'})
    except Exception:
        return json.dumps({'message': 'failed'})


if __name__ == '__main__':
    load()
    app.run(host='10.74.28.4', port=443)