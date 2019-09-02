import pymssql
import json

IP_PORT_INFO = '10.74.16.73'
USERNAME = 'sa'
PASSWORD = 'nb81890!@#'
DATABASE = 'NB81890APP'

SQL_ITEM = 'SELECT ENTERPRISE_ID, ORG_ID, SERV_ITEM_CODE, TITLE FROM T_SHOPITEM WHERE TITLE IS NOT NULL'
SQL_TYPE = 'SELECT CODE, SERVICETYPEVALUE, KEYWORD FROM ST_SERVICE_TYPE WHERE SERVICETYPEVALUE IS NOT NULL OR KEYWORD IS NOT NULL'

ITEM_JSON_PATH = '/home/huper/wordplace/virtual/81890/data/update/sqlserver/item.json'
TYPE_JSON_PATH = '/home/huper/wordplace/virtual/81890/data/update/sqlserver/type.json'


def connect():
    db = pymssql.connect(IP_PORT_INFO, USERNAME, PASSWORD, DATABASE)
    return db.cursor()


def fetch_item(cur):
    cur.execute(SQL_ITEM)
    rows = cur.fetchall()
    lis = []
    for row in rows:
        lis.append({'ENTERPRISE_ID': row[0], 'ORG_ID': row[1], 'CODE': row[2], 'TITLE': row[3]})
    result = {"RECORDS": lis}
    with open(ITEM_JSON_PATH, 'w') as out_file:
        json.dump(result, out_file)


def fetch_type(cur):
    cur.execute(SQL_TYPE)
    rows = cur.fetchall()
    lis = []
    for row in rows:
        lis.append({'CODE': row[0], 'SERVICETYPEVALUE': row[1], 'KEYWORD': row[2]})
    result = {"RECORDS": lis}
    with open(TYPE_JSON_PATH, 'w') as out_file:
        json.dump(result, out_file)


def fetch_and_write():
    cur = connect()
    fetch_item(cur)
    fetch_type(cur)


if __name__ == '__main__':
    fetch_and_write()
