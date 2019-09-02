#!/usr/bin/env bash

nohup ./venv/bin/bert-serving-start -model_dir ./data/model -num_worker=4 -max_seq_len=100 >> bert.log  2>&1 &
nohup ./venv/bin/python ./enter_recall/serving/server.py >> server.log  2>&1 &
/home/huper/wordplace/virtual/81890/venv/bin/python /home/huper/wordplace/virtual/81890/enter_recall/update/update.py >> /home/huper/wordplace/virtual/81890/update.log 2>&1 &
10 1 * * * /home/huper/wordplace/virtual/81890/venv/bin/python /home/huper/wordplace/virtual/81890/enter_recall/update/update.py >> /home/huper/wordplace/virtual/81890/update.log 2>&1