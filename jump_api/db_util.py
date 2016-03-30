# coding:utf8
from MySQLdb import cursors, Connect
from MySQLdb.cursors import DictCursor as DC
from crpt import CRYPTOR
from settings import *


def get_conn():
    print 'host = ', host
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


def update_asset(ip, port, account, passwd, password, checkCode):
    conn = get_conn()
    cursor = conn.cursor()
    tmpl_sql = "update jasset_asset set ip='%s', port='%s',username='%s',passwd='%s',password='%s',check_code='%s' where ip = '%s';"
    cursor.execute(tmpl_sql % (ip, port, account, passwd, password, checkCode, ip))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def insert_asset(ip, port, account, passwd, password, checkCode):
    conn = get_conn()
    cursor = conn.cursor()
    tmpl_sql = "insert into jasset_asset (ip,hostname, port,username,passwd,password,check_code) " \
               "values ('%s','%s','%s','%s','%s','%s','%s');"
    cursor.execute(tmpl_sql % (ip, ip, port, account, passwd, password, checkCode))
    conn.commit()
    cursor.close()
    conn.close()
    return True


if __name__ == '__main__':
    """
    222.187.223.233 22 root
    218.75.159.115 22 root
    """
    # test()
    # count = check_exists('218.75.159.1151')
    # print count
    password = '123456'
    # password_encode = 'ssss'
    password_encode = CRYPTOR.encrypt(password)
    insert_asset('1.1.1.2', '2000', 'account1', password, password_encode, '9999')
    pass
