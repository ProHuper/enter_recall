from flask import Flask
from flask import request
from enter_recall.recall import recall_and_rank

import json

app = Flask(__name__)

item_dict = None
type_dict = None
parent_vocab = None
sim_vocab = None


def load():
    global item_dict, type_dict
    item_dict, type_dict = recall_and_rank.init_dicts()
    global sim_vocab, parent_vocab
    parent_vocab, sim_vocab = recall_and_rank.init_vocabs()


@app.route('/api/query', methods=['GET'])
def query():
    sentence = request.args.get("sentence")
    limits = request.args.get("limits")
    org_id = request.args.get("org")
    return recall_and_rank.query_request(sentence,
                                         int(limits),
                                         int(org_id),
                                         item_dict=item_dict,
                                         type_dict=type_dict,
                                         par_dict=parent_vocab,
                                         sim_dic=sim_vocab)


@app.route('/api/update', methods=['GET'])
def update():
    try:
        load()
        return json.dumps({'message': 'succeed'})
    except:
        return json.dumps({'message': 'failed'})


if __name__ == '__main__':
    load()
    # app.run(host='10.74.28.4', port=443)
    app.run(host='localhost', port=8000)
