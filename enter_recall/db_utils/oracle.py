import cx_Oracle
import json

DB_NAME = ''
IP_PORT_INFO = '222.29.2.29:15210'
SERVICE_NAME = '/ORCL'
USERNAME = '"81890_STUDENT"'
PASSWORD = '81890_STUDENT'
SQL_ENTER_INFO = 'SELECT ID, NAME, ADDRESS, PHONE, SERVICEINFO FROM "T_ENTERPRISE" WHERE SERVICEINFO IS NOT NULL'
SQL_TYPE_TO_CODE = 'SELECT SMALLTYPE, CODE FROM "ST_SERVICETYPE"'
SQL_CODE_TO_ID = 'SELECT ENTERPRISEID, SERVITEMCODE FROM "T_ENTERPRISE_SERVICE"'

ENTER_JSON_PATH = '../../data/update/oracle/enter/enter.json'
TYPE_TO_CODE_PATH = '../../data/update/oracle/type/type2code.json'
CODE_TO_ID_PATH = '../../data/update/oracle/type/code2id.json'


def connect():
    db = cx_Oracle.connect(USERNAME, PASSWORD, IP_PORT_INFO + SERVICE_NAME, encoding='UTF-8')
    return db.cursor()


def fetch_enter(cur):
    cur.execute(SQL_ENTER_INFO)
    rows = cur.fetchall()
    lis = []
    for row in rows:
        lis.append({'ID': row[0], 'NAME': row[1], 'ADDRESS': row[2], 'PHONE': row[3], 'SERVICEINFO': row[4]})
    result = {"RECORDS": lis}
    with open(ENTER_JSON_PATH, 'w') as out_file:
        json.dump(result, out_file)


def fetch_type2code(cur):
    cur.execute(SQL_TYPE_TO_CODE)
    rows = cur.fetchall()
    lis = []
    for row in rows:
        lis.append({'SMALLTYPE': row[0], 'CODE': row[1]})
    result = {"RECORDS": lis}
    with open(TYPE_TO_CODE_PATH, 'w') as out_file:
        json.dump(result, out_file)


def fetch_code2id(cur):
    cur.execute(SQL_CODE_TO_ID)
    rows = cur.fetchall()
    lis = []
    for row in rows:
        lis.append({'ENTERPRISEID': row[0], 'SERVITEMCODE': row[1]})
    result = {"RECORDS": lis}
    with open(CODE_TO_ID_PATH, 'w') as out_file:
        json.dump(result, out_file)


def fetch_and_write():
    cur = connect()
    fetch_enter(cur)
    fetch_type2code(cur)
    fetch_code2id(cur)
