# coding:utf8
from MySQLdb import cursors, Connect
from MySQLdb.cursors import DictCursor as DC
from settings import *


def get_conn():
    return Connect(host=host, user=user, passwd=password, db=database, compress=1, cursorclass=DC, charset='utf8')


def test():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT ip, port, username FROM jasset_asset limit 10;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in rows:
        print row['ip'], row['port'], row['username']


def check_exists(ip):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT count(1) FROM jasset_asset where ip = '%s';" % ip)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return bool(int(rows[0]['count(1)']))

def update_asset(ip, port, account, password, checkCode):
    conn = get_conn()
    cursor = conn.cursor()
    tmpl_sql = "update jasset_asset set ip='%s', port='%s',username='%s',passwd='%s',password='%s',check_code='%s';"
    cursor.execute(tmpl_sql % (ip, port, account, password, checkCode))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return bool(int(rows[0]['count(1)']))

def insert_asset():
    pass


if __name__ == '__main__':
    """
    222.187.223.233 22 root
    218.75.159.115 22 root
    """
    # test()
    count = check_exists('218.75.159.1151')
    print count
    pass
